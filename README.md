# S3-bucket-tool

## Running it

1. First you'll need to create an AWS account. One can be created for free.
2. Create an S3 bucket and upload some files into it. Bear in mind that there can be a charge if you go over the
[free tier requirements](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all&all-free-tier.q=S3&all-free-tier.q_operator=AND)
(5 GiB at time of writing).
3. To run the project itself, you'll need Python 3.8 and [Poetry](https://python-poetry.org/docs/#installation)
4. Run `poetry install`
5. Make sure you have configured your terminal with aws-cli to have loaded credentials that the tool will use
6. Run `poetry run cli --help`

### Useful dev commands
To run formatter
`poetry run black .`

To run tests
`poetry run pytest .`

### Available features
#### list
To list all buckets in the account run 
`poetry run cli list`
You can also specify the wanted size unit for files with the `--size-format` flag. Available values are `b|kb|mb|gb|tb`
You can also provide a grouping options with the `--group-by` flag. Only the `region` value is supported

#### get
You can display information of a specific bucket with the get command by providing the name of the bucket
`poetry run cli get BUCKET_NAME`
You can also provide the `--size-format` flag like in the list command

#### find
You can search for specific buckets either by bucket name or by storage class
`poetry run cli find --name=BUCKET_NAME`
or
`poetry run cli find --storage-class=STORAGE_CLASS`
You can also provide the `--size-format` flag like in the list command
