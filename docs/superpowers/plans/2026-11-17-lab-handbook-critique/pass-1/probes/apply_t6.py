import json
b=json.load(open('probes/t6.json',encoding='utf-8'))
p='hb/curriculum/ph21x/ph21x-lab-handbook.md'; s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1, old
    s=s.replace(old,new)
rep('title: "Appendix B – Reference Information"\n','title: "Lab Handbook"\n')
rep('status: converted\n','status: ruled-change\n')
rep('    ledger: "D-0188"\nimages:\n','    ledger: "D-0188"\n'+b[1]+'images:\n')
rep('\n# Appendix B – Reference Information\n','\n# Lab Handbook\n')
rep('\nThis section contains key information from previous labs:\n',
    '\nEvery lab after the first uses the ideas on this page. Read it before you start a lab, and come back whenever a lab asks for a plot, a fit or an uncertainty.\n')
old='''1.  Required Plot Elements
2.  Linearization
3.  What is Uncertainty?
4.  Sources of Uncertainty
5.  Predictions, Hypotheses, and Models
6.  Tips for Using Graphical Analysis
7.  Variables and Parameters
'''
rep(old,b[2])
open(p,'w',encoding='utf-8',newline='\n').write(s)
