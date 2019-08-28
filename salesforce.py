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
        success = collections.defaultdict()

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
        current = Module.get_instance(Module(depName),depName)

        for str_dependancy in args[1:]:
            dependancy = Module.get_instance(Module(depName),str_dependancy)
            current.add_dependancy(dependancy)
            dependancy.add_dependant(current)
        return {}


class InstallCmd(object):
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        result = collections.defaultdict()

        for depName in args:
            dependancy_module = Module.get_instance(Module(depName),depName)
            self.install(dependancy_module,result)
        return result

    def install(self,current,result):
        if not current.is_installed():
            current.set_installed = True
            print(current,current.set_installed)

            for dependancy in current.get_dependencies():
                if not dependancy.is_installed():
                    self.install(dependancy,result)

            result[current.get_name()] = 'succesfully installed'
        else:
            result[current.get_name()] = 'is already installed'

        return result

class RemoveCmd:
    pass

class ListCmd(object):
    def __init__(self,args=None):
        self.args = args

    def execute(self,args):
        result = collections.defaultdict()

        for module in Module.get_installed():
            print(module)
            result[module.get_name()] = ''
        return result


class Module(object):
    DEPENDANCY_MAP = collections.defaultdict()
    def __init__(self,name):
        self.name = name
        self.dependencies = set()
        self.dependants = set()
        self.installed = None

    def get_instance(self,name):
        target = Module.DEPENDANCY_MAP.get(name)
        print("target is:{0}".format(target))
        #target = self.dependancymap.get(name)
        if not target:
            target = Module(name)
            Module.DEPENDANCY_MAP[name] = target
            #self.dependancymap[name] = target
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
            print(module.is_installed())
            if module.is_installed():
                installed.add(module)
        print("installed modules are:{0}".format(installed))
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