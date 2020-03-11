import subprocess
import sys
from environments import Environments


class QuickStart:
    def __init__(self, _root_path):
        self.root_path = _root_path
        self.entry = ''
        self.env = Environments(_root_path).env

    def run(self):
        print(self.__class__.__name__, self.root_path)
        success = True
        print('prepare...')
        _out, _err = self.prepare()
        print(_out)
        print(_err, file=sys.stderr)
        if len(_err) > 0:
            success = False
        if success:
            print('execute...')
            _out, _err = self.execute()
            print(_out)
            print(_err, file=sys.stderr)
            if len(_err) > 0:
                success = False
        print('clear...')
        _out, _err = self.clear()
        print(_out)
        print(_err, file=sys.stderr)
        if len(_err) > 0:
            success = False
        return success

    def prepare(self):
        return '', ''

    def execute(self):
        return '', ''

    def clear(self):
        return '', ''

    def _run_shell(self, args):
        _out = subprocess.Popen(args,
                                env=self.env,
                                shell=True,
                                cwd=self.root_path,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        return (x.decode('utf-8') for x in _out.communicate())


class JavascriptQuickStart(QuickStart):
    def __init__(self, _root_path):
        super().__init__(_root_path)

    def prepare(self):
        return self._run_shell(['npm', 'install'])

    def execute(self):
        return self._run_shell(['npm', 'start'])


class PythonQuickStart(QuickStart):
    def __init__(self, _root_path, entry_file):
        super().__init__(_root_path)
        self.entry = entry_file

    def prepare(self):
        self._run_shell(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
        return self._run_shell(['pip', 'install', '-r', 'requirements.txt'])

    def execute(self):
        return self._run_shell(['python', self.entry])


class JavaQuickStart(QuickStart):
    def __init__(self, _root_path):
        super().__init__(_root_path)

    def prepare(self):
        return self._run_shell(['mvn', '-q', 'compile'])

    def execute(self):
        return self._run_shell(['mvn', '-q', 'exec:java'])


class DotnetQuickStart(QuickStart):
    def __init__(self, _root_path, project_file):
        super().__init__(_root_path)
        self.entry = project_file
        '''
            def prepare(self):
                return self._run_shell(['dotnet', 'restore', self.entry])
        '''

    def execute(self):
        return self._run_shell(['dotnet', 'run', '--project', self.entry])
