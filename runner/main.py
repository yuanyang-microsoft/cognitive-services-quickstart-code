import os
from quickstarts import JavascriptQuickStart, PythonQuickStart, JavaQuickStart, DotnetQuickStart


def get_quickstarts_by_beacons(base_path, beacon):
    for sample in os.listdir(base_path):
        sub_path = '{}/{}'.format(base_path, sample)
        if os.path.exists('{}/{}'.format(sub_path, beacon)):
            yield sub_path
        elif os.path.isdir(sub_path):
            for x in get_quickstarts_by_beacons(sub_path, beacon):
                yield x


def get_quickstarts_by_extension(base_path, extension):
    for sample in os.listdir(base_path):
        sub_path = '{}/{}'.format(base_path, sample)
        if os.path.isdir(sub_path):
            for x in get_quickstarts_by_extension(sub_path, extension):
                yield x
        elif sub_path.endswith(extension):
            yield base_path, sample


def get_quickstarts_of_javascript():
    for quickstart in get_quickstarts_by_beacons('../javascript', 'package.json'):
        yield JavascriptQuickStart(quickstart)


def get_quickstarts_of_java():
    for quickstart in get_quickstarts_by_beacons('../java', 'pom.xml'):
        yield JavaQuickStart(quickstart)


def get_quickstarts_of_python():
    for quickstart in get_quickstarts_by_beacons('../python', 'requirements.txt'):
        for sample_file in os.listdir(quickstart):
            if sample_file.endswith('.py'):
                yield PythonQuickStart(quickstart, sample_file)


def get_quickstarts_of_dotnet():
    for path, csproj in get_quickstarts_by_extension('../dotnet', '.csproj'):
        yield DotnetQuickStart(path, csproj)


def get_quickstarts():
    yield from get_quickstarts_of_dotnet()
    yield from get_quickstarts_of_java()
    yield from get_quickstarts_of_python()
    yield from get_quickstarts_of_javascript()


if __name__ == "__main__":

    # whitelist = {'../dotnet/BingAutoSuggest', '../java/ComputerVision'}
    whitelist = {}

    for quick_start in get_quickstarts():
        print(quick_start.root_path, quick_start.entry)
        if quick_start.root_path in whitelist:
            print(quick_start.run())


