# finops-crawler

This project is active. Development is ongoing, and contributions are welcome (see below).

## Basic Usage

This package is designed to fetch cost/usage data from various platforms (Azure, AWS, OpenAI, and more to follow).

**The main principle is to have as simple an approach as possible along with the absolute minimum set of permissions required**. Thus, the quickstart part of each guide is presented as CLI commands.

The result, for now, is a Python variable as returned by the API or SDK.

### Platform-specific documentation

Each platform is different and has a separate guide on how to set up an entity with minimum permissions to read the cost data. Specific code snippets to get started are included.

- [Azure](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/azure)
- [AWS](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/aws)

No longer works, need to wait for explicit usage API:
- [OpenAI](https://github.com/finops-fitness-club/finops-crawler/tree/main/src/finops_crawler/openai)


### Overview of the flow

1. Set up a user (technical user/service principal) for querying the data
2. Set up permissions for that user
3. Set environment variables to be used by the package
4. Use the package

### Resulting data

Each platform has its own format. Also, the same date range might produce different results depending on the platform. Some might include the last day, some may not.

There is an open data specification being developed by FinOps Foundation ([FOCUS](https://focus.finops.org/)). At this point, it's still very new and not adopted by the industry. We will keep a close eye on it and support it as soon as feasible.

*Note*: querying long time periods might trigger paginated results. AWS and Azure handle it correctly. OpenAI does not have paginated results as it's an undocumented API and it also has not existed yet for a very long time.

### Plans

Increase breath by expanding to various other tools and platforms (Databricks, GCP, etc.)

Increase depth by implementing `save_to_postgres` or similar functionality to actually store it.

### Contributing

Got ideas for improvements? We'd love your input!

1. Fork and clone this repository.
2. Optionally, choose an issue labeled as "help wanted" or "good first issue".
3. Submit a pull request with your changes and a clear description.

Remember, all contributions from bug fixes to documentation updates are greatly appreciated!

Enjoy :)

Email: finops.fitness.club@gmail.com
