from prefect.filesystems import GitHub


gh_repo = GitHub(repository="https://github.com/davidag/data-engineering-zoomcamp.git")
gh_repo.save("de-zoomcamp-personal-repo", overwrite=True)
