"""Arketype Windows UI; Python and Tkinter must be available."""
from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arketype import catalogue,assemblies,create,render_archetype

archs={a['slug']:a for a in catalogue()}
recipes={r['id']:r for r in assemblies()}
root=tk.Tk()
root.title('Arketype')
root.geometry('850x690')
root.columnconfigure(1,weight=1)

# Brand identity belongs to the UI, not to the repository README.
header = tk.Frame(root, bg='#f2f8f6', padx=16, pady=12)
header.grid(row=0, column=0, columnspan=2, sticky='ew')
header.columnconfigure(1, weight=1)
try:
    brand_icon = tk.PhotoImage(file=str(Path(__file__).resolve().parent / 'assets' / 'logo-k-ui.png'))
    tk.Label(header, image=brand_icon, bg='#f2f8f6').grid(row=0, column=0, rowspan=2, sticky='w', padx=(0, 18))
except (tk.TclError, OSError):
    tk.Label(header, text='K', font=('Segoe UI', 28, 'bold'), fg='#1e6864', bg='#f2f8f6').grid(row=0, column=0, rowspan=2, padx=(0, 18))
tk.Label(header, text='ARKETYPE', font=('Segoe UI', 21, 'bold'), fg='#1e6864', bg='#f2f8f6').grid(row=0, column=1, sticky='w')
tk.Label(header, text='Kristal archetype library · Local creation', font=('Segoe UI', 10), fg='#477671', bg='#f2f8f6').grid(row=1, column=1, sticky='w')

selection=tk.StringVar(value=next(iter(archs)))
recipe=tk.StringVar(value='None')
slug=tk.StringVar()
title=tk.StringVar()
parent=tk.StringVar()


def set_description(event=None):
    desc.config(state='normal')
    r = recipes.get(recipe.get())
    if r:
        selection.set(r['primary_archetype'])
    desc.delete('1.0','end')
    desc.insert('end',render_archetype(archs[selection.get()]))
    if r:
        desc.insert('end','\n\nAssembly: '+r['title']+'\n')
        for c in r['components']:
            desc.insert('end','  + '+c['archetype']+' ['+c['relation']+']\n')
        desc.insert('end','\nDesign-only plan; canonical states are never merged.\n')
    desc.config(state='disabled')

for i,label in enumerate(('Primary archetype','Optional assembly','Kristal slug','Kristal title','Parent directory')):
    ttk.Label(root,text=label).grid(row=i+1,column=0,sticky='w',padx=12,pady=8)
types_widget=ttk.Combobox(root,textvariable=selection,values=list(archs),state='readonly',width=40)
types_widget.grid(row=1,column=1,padx=8,sticky='ew')
types_widget.bind('<<ComboboxSelected>>',lambda ev:(recipe.set('None'),set_description()))
recipes_widget=ttk.Combobox(root,textvariable=recipe,values=['None',*recipes],state='readonly')
recipes_widget.grid(row=2,column=1,padx=8,sticky='ew')
recipes_widget.bind('<<ComboboxSelected>>',set_description)
ttk.Entry(root,textvariable=slug).grid(row=3,column=1,padx=8,sticky='ew')
ttk.Entry(root,textvariable=title).grid(row=4,column=1,padx=8,sticky='ew')
f=ttk.Frame(root); f.grid(row=5,column=1,padx=8,sticky='ew'); f.columnconfigure(0,weight=1)
ttk.Entry(f,textvariable=parent).grid(row=0,column=0,sticky='ew')
ttk.Button(f,text='Browse…',command=lambda:parent.set(filedialog.askdirectory() or parent.get())).grid(row=0,column=1,padx=(8,0))

desc=tk.Text(root,height=16,wrap='word',font=('Segoe UI',10))
desc.grid(row=6,column=0,columnspan=2,padx=12,pady=12,sticky='nsew')
root.rowconfigure(6,weight=1)


def submit():
    try:
        picked=recipe.get() if recipe.get()!='None' else None
        p=create(selection.get(),slug.get().strip(),title.get().strip(),parent.get().strip(),recipe=picked)
        messagebox.showinfo('Arketype — Created','Neutral workspace checked: \n'+str(p)+'\n\nNo domain facts or publication added.')
    except Exception as e:messagebox.showerror('Arketype — Creation failed',str(e))

ttk.Label(root,text='Local creation only · noncanonical design · no publication').grid(row=7,column=0,columnspan=2,pady=5)
ttk.Button(root,text='Create Kristal',command=submit).grid(row=8,column=0,columnspan=2,pady=12)
set_description()
root.mainloop()
