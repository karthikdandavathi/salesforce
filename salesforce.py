import collections

class JumpStart(object):
    def __init__(self,lines):
        self.lines = lines
        self.commands = {'DEPEND': DependCmd(), 'INSTALL': InstallCmd(), 'REMOVE': RemoveCmd(), 'LIST': ListCmd()}
        self.process(lines)

    def process(self,lines):
        for line in lines:
            if line == 'END':
                print(line)
                break
            else:
                self.process_line(line)

    def process_line(self,line):
        print(line)
        args = line.split(' ')
        cmd = self.commands.get(args[0])
        success = collections.OrderedDict()

        #remove cmd argument from list
        args.pop(0)
        success = cmd.execute(args)
        for k,v in success.items():
            print("\t" + k + " " + v)


class DependCmd(object):
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        depName = args[0]

        #get current module
        current = Module.get_instance(depName)

        for str_dependancy in args[1:]:
            dependancy = Module.get_instance(str_dependancy)
            current.add_dependancy(dependancy)
            dependancy.add_dependant(current)
        return {}


class InstallCmd(object):
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        result = collections.OrderedDict()

        for depName in args:
            dep = Module.get_instance(depName)
            self.install(dep,result)
        return result

    def install(self,current,result):
        if not current.is_installed():
            current.set_installed(True)

            for dependancy in current.get_dependencies():
                if not dependancy.is_installed():
                    self.install(dependancy,result)
            result[current.get_name()] = 'succesfully installed'
        else:
            result[current.get_name()] = 'is already installed'
        return result

class RemoveCmd:
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        depName = args[0]

        dep = Module.get_instance(depName)
        if dep is not None:
            return self.uninstall(dep,True)

        result[depName] = 'is not installed'
        return result

    def uninstall(self,parent,children):
        result = collections.OrderedDict()
        #get installed dependants
        if parent.is_installed():
            installed_dependants = set()

            tmp = parent.get_dependants()
            for dep in tmp:
                if dep.is_installed():
                    installed_dependants.add(dep)

            if not installed_dependants:
                if not children:
                    result[parent.get_name()+ ' is no longer needed'] = ''
                result[parent.get_name()] = ' succesfully removed'
                parent.set_installed(False)

                if children:
                    for dependancy in parent.get_dependencies():
                        if dependancy.is_installed():
                            result.update(self.uninstall(dependancy,False))
            else:
                if children:
                    result[parent.get_name()] = 'is still needed'
        else:
            result[parent.get_name()] = 'is not installed'
        return result


class ListCmd(object):
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        result = collections.OrderedDict()

        for module in Module.get_installed():
            result[module.get_name()] = ''
        return result


class Module(object):
    DEPENDANCY_MAP = collections.OrderedDict()
    def __init__(self,name):
        self.name = name
        self.dependencies = set()
        self.dependants = set()
        self.installed = None

    @staticmethod
    def get_instance(name):
        target = Module.DEPENDANCY_MAP.get(name)
        if not target:
            target = Module(name)
            Module.DEPENDANCY_MAP[name] = target
        return target

    def get_name(self):
        return self.name

    def is_installed(self):
        return self.installed

    def set_installed(self,installed):
        self.installed = installed

    def get_dependants(self):
        return self.dependants

    def get_dependencies(self):
        return self.dependencies

    def add_dependancy(self,module):
        return self.dependencies.add(module)

    def add_dependant(self,module):
        return self.dependants.add(module)

    @classmethod
    def get_installed(cls):
        installed = set()

        for module in cls.DEPENDANCY_MAP.values():
            if module.is_installed():
                installed.add(module)
        return installed


if __name__ == '__main__':
    lines = []
    while True:
        line = raw_input()
        if line:
            lines.append(line.strip())
        else:
            break
    start = JumpStart(lines)
