import parser

##networkx

if __name__ == "__main__":
    import cli
    from plot import Plot

    parser = cli.init_parser()
    args = parser.parse_args()
    data = cli.parse_datafile(args.filename)

    Plot(
        title=data["titles"],
        xlabel=data["xlabel"],
        ylabel=data["ylabel"],
        x=data["x"],
        values=data["y"],
    ).save(args.name)
