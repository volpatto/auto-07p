#!/usr/bin/env autox
import windowPlotter
import parseB
import parseS
import matplotlib
import code
import re
import sys
import string
import Tkinter

class PyPlautInteractiveConsole(code.InteractiveConsole):
    def __init__(self,locals=None,b=None,s=None):
        code.InteractiveConsole.__init__(self,locals)
        if locals is None:
            return
        
        self.line_split = re.compile(r'^(\s*[,;/]?\s*)'
                                     r'([\?\w\.]+\w*\s*)'
                                     r'(\(?.*$)')
        self.re_exclude_auto = re.compile(r'^[<>,&^\|\*/\+-]'
                                          '|^is |^not |^in |^and |^or ')
        self.state = ''
        self.xaxis = 1
        self.yaxis = 2
        self.expert = None

        root=Tkinter.Tk()
        root.withdraw()
        self.handle = windowPlotter.WindowPlotter2D(root,
            {},grapher_bifurcation_diagram=b,
            grapher_solution=s,
            grapher_width=600,grapher_height=480)
        self.xlabel = self.handle.config("xlabel")[3]
        if self.xlabel is None:
            self.xlabel = ""
        self.ylabel = self.handle.config("ylabel")[3]
        if self.ylabel is None:
            self.ylabel = ""
        self.handle.config(xlabel=self.xlabel,ylabel=self.ylabel)
        self.handle.update()

    def raw_input(self, prompt=None):
        line = ""
        while 1:
            if line == "":
                print " ENTER COMMAND\n"
                line = raw_input(prompt)
            line = self.process_input(line)

    def process_input(self, line):
        lower = 0
        upper = 0
        its = 0
        for c in line:
            if c in string.lowercase:
                lower = 1
            if c in string.uppercase:
                upper = 1
        if upper and not lower:
            line=string.lower(line)
        if line in ["stop","exit","quit","end"]:
            sys.exit()
        elif line in ["scr","screen"]:
            return ""
        elif line in ["ss","set sym"]:
            return ""
        elif line == "sd":
            return ""
        elif line in ["lab","label"]:
            self.listlabels()
            return ""
        elif line in ["c","cl","clr","clear"]:
            self.handle.grapher.clear()
            self.handle.grapher.update()
            return ""
        elif line in ["save","sav","sa","s"]:
            return ""
        elif line == "help":
            return self.help()
        elif line in ["sy","sym","symbol"]:
            return ""
        opts = []
        for j in range(6):
            if len(line) < j*2+2:
                break
            opts.append(line[j*2:j*2+2])
        if "sy" in opts:
            its = 1
        if "dp" in opts:
            its = 1
        if "ax" in opts:
            its = 1
            print ' ENTER HORIZONTAL AND VERTICAL AXIS NUMBER (1,2,...) :'
            [self.xaxis,self.yaxis] = map(int,string.split(raw_input()))
            self["bifurcation_x"] = [self.xaxis-1]
            self["bifurcation_y"] = [self.yaxis-1]
        if "st" in opts:
            self.settitles()
            its = 1
        if "d0" in opts:
            self["grid"] = "no"
            self["use_labels"] = 1
            #do not show stability
            its = 1
        if "d1" in opts:
            self["grid"] = "no"
            self["use_labels"] = 1
            #show stability
            its = 1
        if "d2" in opts:
            self["grid"] = "no"
            self["use_labels"] = 0
            #show stability
            its = 1
        if "d3" in opts:
            self["grid"] = "yes"
            self["use_labels"] = 1
            #show stability
            its = 1
        if "d4" in opts:
            self["grid"] = "yes"
            self["use_labels"] = 0
            #show stability
            its = 1
        if "nu" in opts:
            its = 1
        if "xp" in opts:
            its = 1
        if "bd" in opts:
            its = 1
            self.plotbif(b)
            return ""
        elif "bd0" in opts:
            its = 1
            self.plotbif(b)
            return ""
        elif line[:2] == "2d":
            self.plotsol(s)
            return ""
        elif line == "sda":
            return ""
        elif line == "sdo":
            return ""
        elif line == "sci":
            return ""
        elif line == "ssy":
            return ""
        elif line == "pa":
            return ""
        elif line == "sdd":
            return ""
        elif line == "sls":
            return ""
        elif line == "lda":
            return ""
        elif line == "us":
            return ""
        elif line == "lls":
            return ""
        elif line == "rss":
            return ""
        elif line == "rcs":
            return ""
        elif line == "res":
            return ""
        if its == 0:
            print ' ILLEGAL COMMAND - REENTER'
        return ""

    def settitles(self):
        if not self.expert:
            print ' ENTER X AXIS LABEL BETWEEN THE QUOTES'
        print ' "                              "'
        self.xlabel = raw_input().strip()
        self["xlabel"] = self.xlabel

        if not self.expert:
            print ' ENTER Y AXIS LABEL BETWEEN THE QUOTES'
        print ' "                              "'
        self.ylabel = raw_input().strip()
        self["ylabel"] = self.ylabel

        ax = self.handle.grapher.ax
        if not self.expert:
            print ' ENTER TOP TITLE BETWEEN THE QUOTES'
        print ' "                                                            "'
        ax.set_title(raw_input().strip())
        self.handle.grapher.update()

        #if not self.expert:
        #    print ' ENTER BOTTOM TITLE BETWEEN THE QUOTES'
        #print ' "                                                            "'
        #ax.text(0.5,0,raw_input().strip(),transform=ax.transAxes)
        #self.handle.grapher.canvas.show()

    def listlabels(self):
        s = self["solution"]
        i = 0
        str='\n  THE LABELS ARE :    '
        for label in s.getLabels():
            str=str+"%5d"%(label)
            i=i+1
            if i==10:
                print str
                str='                      '
                i=0
        if len(str) > 22:
            print str

    def plotsol(self,name):
        self["type"] = "solution"
        self.listlabels()
        print '\n ENTER LABELS, OR <A> (ALL)\n'
        line = string.lower(raw_input())
        if line[0] == 'a':
            self["label"] = s.getLabels()
        else:
            self["label"] = map(int,string.split(line))
        self.ndim=len(s[0]["data"][0]['u'])+1
        self.xaxs = 1
        self.yaxs = 2
	while 1:
	    lower = 0
            upper = 0
            its = 0
            for c in line:
                if c in string.lowercase:
                    lower = 1
                if c in string.uppercase:
                    upper = 1
            if upper and not lower:
                line=string.lower(line)
            print '  NUMBER OF COMPONENTS :%5d'%(self.ndim)
            print ('  ENTER AXES  (DEFAULT %3d%3d),'\
                   ' <D> (DISPLAY), OR <EX> (EXIT)'%(self.xaxs,self.yaxs))
            line = raw_input()
            if line == 'ex':
                return
            elif line == 'd':
                pass
            else:
                try:
                    [self.xaxs,self.yaxs] = map(int,string.split(line))
                    if self.xaxs == '1':
                        self.xaxs = 't'
                    else:
                        self.xaxs = self.xaxs - 2
                    if self.yaxs == '1':
                        self.yaxs = 't'
                    else:
                        self.yaxs = self.yaxs - 2
                    self["solution_x"] = [self.xaxs]
                    self["solution_y"] = [self.yaxs]
                except:
                    pass

    def plotbif(self,name):
        self.handle.config(type = "bifurcation",
                           xlabel = self.xlabel, ylabel = self.ylabel)
        
    def __setitem__(self,key,value):
        self.handle[key] = value

    def __getitem__(self,key):
        return self.handle[key]

    def help(self):
        print """
         Principal PLAUT Commands :

  <BD0>   Bifurcation diagram with default limits
  <BD>    Bifurcation diagram with user-limits
  <AX>    To select bifurcation diagram axes
  <2D>    2D plot of labeled solutions
  <SAV>   To save the current plot in a file
  <CL>    To clear the graphics window
  <LAB>   List all labeled solutions in Unit 8
  <END>   To End PLAUT

        PLAUT Default Options :

  <D0>    Use solid curves, labels, symbols
  <D1>    As <D0>, showing stability
  <D2>    As <D1>, without labels
  <D3>    As <D1>, with grid lines
  <D4>    AS <D2>, with grid lines

        Individual Options :

  <SY>    Use symbols for special points
  <DP>    Differential Plot (show stability)
  <ST>    Set up titles and axes labels
  <NU>    Normal usage (Reset special options)

  Press RETURN for more or Enter Command ...
  """
        line = raw_input()
        if line != "":
            return line
        print """
        Additional PLAUT Commands :

  <SCR>   To change the plot size
  <SS>    To define symbols
  <RSS>   Set symbol size
  <XP>    ""Expert"" (Abbreviated prompts)
  <SD>    To change curve type

  <SDA>   Set dash spacing
  <LDA>   Set dash size
  <SDO>   Set dot spacing
  <SCI>   Set circle spacing
  <SSY>   Set curve-symbol spacing
  <RCS>   Set curve-symbol size
  <SDD>   Set dash-dot spacing
  <SLS>   Set long-short dash spacing
  <LLS>   Set long-short dash size
  <PA>    Set plotting accuracy
  <RES>   Reset curves and symbols

         --- End of Help ---
  """
        return ""

# Export the functions inside AUTOSimpleFunctions in a dictionary
# This also allows the setting of the log
def exportFunctions(log=None):
    PyPlautFunctionsInstance = PyPlautInteractiveConsole()
    dict = {}
    for name in PyPlautInteractiveConsole.__dict__.keys():
        if name[0] != '_':
            dict[name] = getattr(PyPlautFunctionsInstance, name)
    return dict

# This is the Python syntax for making a script runable    
if __name__ == '__main__':
    try:
        import readline
    except:
        pass

    sys.ps1=""
    if len(sys.argv) < 2:
        b='fort.7'
        s='fort.8'
    else:
        b='b.'+sys.argv[1]
        s='s.'+sys.argv[1]
    b = parseB.parseB(b)
    s = parseS.parseS(s)
    runner = PyPlautInteractiveConsole(exportFunctions(), b, s)
    runner.interact(" ENTER <HELP> IN CASE OF DIFFICULTY\n")
