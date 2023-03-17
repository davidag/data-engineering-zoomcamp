import argparse
import sys
import csv
from pathlib import Path

from confluent_kafka import Producer
from config import config



class CSVProducer:
    def __init__(self, filename: str, props: dict):
        self.filepath = Path(filename)
        self.producer = Producer(props)

    @property
    def topic(self):
        return self.filepath.name.split(".")[0]

    def run(self):
        for row in self.read_records():
            key = row[0]  # assume first column is always the key
            value = ",".join(row[1:])  # the rest is the value
            try:
                self.producer.produce(
                    topic=self.topic,
                    key=key,
                    value=value,
                    callback=CSVProducer.delivery_callback
                )
            except KeyboardInterrupt:
                break
            except BufferError:
                sys.stderr.write(f"%% Local producer queue is full ({len(self.producer)} messages awaiting delivery): try again\n")

            self.producer.poll(0)

        self.producer.flush()

    def read_records(self):
        with open(self.filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip first line
            for row in reader:
                yield row

    @staticmethod
    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message \'%s\' delivered to %s [%d] @ %d\n' %
                             (msg.key(), msg.topic(), msg.partition(), msg.offset()))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce records from csv file")
    parser.add_argument("--csvfile", "-f", type=str, required=True, help="CSV file")
    args = parser.parse_args()

    producer = CSVProducer(args.csvfile, config)
    producer.run()
