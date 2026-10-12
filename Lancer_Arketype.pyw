"""Interface Windows simple de Arketype; Python et Tkinter doivent être disponibles."""
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
root.geometry('800x580')
root.columnconfigure(1,weight=1)

selection=tk.StringVar(value=next(iter(archs)))
recipe=tk.StringVar(value='Aucun')
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
        desc.insert('end','\n\nAssemblage : '+r['title']+'\n')
        for c in r['components']:
            desc.insert('end','  + '+c['archetype']+' ['+c['relation']+']\n')
        desc.insert('end','\nPlan conceptuel seulement, sans fusion du canon.\n')
    desc.config(state='disabled')

for i,label in enumerate(('Archétype principal','Assemblage facultatif','Slug du Kristal','Titre du Kristal','Dossier parent')):
    ttk.Label(root,text=label).grid(row=i,column=0,sticky='w',padx=12,pady=8)
types_widget=ttk.Combobox(root,textvariable=selection,values=list(archs),state='readonly',width=40)
types_widget.grid(row=0,column=1,padx=8,sticky='ew')
types_widget.bind('<<ComboboxSelected>>',lambda ev:(recipe.set('Aucun'),set_description()))
recipes_widget=ttk.Combobox(root,textvariable=recipe,values=['Aucun',*recipes],state='readonly')
recipes_widget.grid(row=1,column=1,padx=8,sticky='ew')
recipes_widget.bind('<<ComboboxSelected>>',set_description)
ttk.Entry(root,textvariable=slug).grid(row=2,column=1,padx=8,sticky='ew')
ttk.Entry(root,textvariable=title).grid(row=3,column=1,padx=8,sticky='ew')
f=ttk.Frame(root); f.grid(row=4,column=1,padx=8,sticky='ew'); f.columnconfigure(0,weight=1)
ttk.Entry(f,textvariable=parent).grid(row=0,column=0,sticky='ew')
ttk.Button(f,text='Parcourir…',command=lambda:parent.set(filedialog.askdirectory() or parent.get())).grid(row=0,column=1,padx=(8,0))

desc=tk.Text(root,height=16,wrap='word',font=('Segoe UI',10))
desc.grid(row=5,column=0,columnspan=2,padx=12,pady=12,sticky='nsew')
root.rowconfigure(5,weight=1)


def submit():
    try:
        picked=recipe.get() if recipe.get()!='Aucun' else None
        p=create(selection.get(),slug.get().strip(),title.get().strip(),parent.get().strip(),recipe=picked)
        messagebox.showinfo('Arketype — création réussie','Workspace neutre vérifié :\n'+str(p)+'\n\nAucun fait métier ni publication ajoutés.')
    except Exception as e:messagebox.showerror('Arketype — impossible de créer',str(e))

ttk.Label(root,text='Création locale uniquement · design non canonique · aucune publication').grid(row=6,column=0,columnspan=2,pady=5)
ttk.Button(root,text='Créer le Kristal',command=submit).grid(row=7,column=0,columnspan=2,pady=12)
set_description()
root.mainloop()
