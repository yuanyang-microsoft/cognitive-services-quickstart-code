import subprocess
import sys
import os

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


class QuickStart:
    def __init__(self, _):
        self.ignore = _['ignore']
        self.root_path = os.path.join('..', _['path'])
        self.entry = _['entry']
        self.env = os.environ.copy()
        self.prepare_parameters(_['parameters'])

    def prepare_parameters(self, parameters):
        for parameter in parameters:
            _name = parameter['name']
            if 'value' in parameter:
                _value = parameter['value']
            elif 'keyVaultUrl' in parameter and 'keyVaultSecret' in parameter:
                credential = ClientSecretCredential('72f988bf-86f1-41af-91ab-2d7cd011db47', '594f2bef-5021-4317-8e5c-f3f1e1117565', os.environ.get('CsdxClientSecret'))
                client = SecretClient(vault_url=parameter['keyVaultUrl'], credential=credential)
                _value = client.get_secret(parameter['keyVaultSecret']).value
            else:
                raise Exception('`value` or `keyVaultUrl+keyVaultSecret` should exist')
            self.env[_name] = _value
        print(self.env)


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
                                shell=False,
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
    def execute(self):
        return self._run_shell(['dotnet', 'run', '--project', self.entry])
