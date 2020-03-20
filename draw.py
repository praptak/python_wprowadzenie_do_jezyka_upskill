import click


@click.command()
@click.option('--file', help='Type participants filename for lottery.')
@click.option('--file_type', default='json',
              help='Type file type for participants file. Choose between "json" and "csv". Default is "json"')
@click.option('--lotttery', default=None,
              help="""
              Provide lottery template name. 
              If not provided, the first one (in alphabetical order) will be chosen.
              """)
def cli(file, file_type, lottery):
    click.echo('Hello World! This is a file: ' + file + '.' + file_type)


if __name__ == '__main__':
    cli()
