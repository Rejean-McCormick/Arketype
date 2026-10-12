"""Arketype Desktop: unified offline catalogue, neutral creator, and safe ops console.

The UI has no remote commands, publication controls, hidden network requests, or
arbitrary shell execution. Tk updates are performed on the GUI thread.
"""
from __future__ import annotations
import json
import queue
from pathlib import Path
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import webbrowser

from arketype import (ROOT, archetype, catalogue, assemblies, create, normalized,
                      render_archetype, render_profile, use_case_profiles)
from arketype_launcher_ops import OperationError, parse_operation, run_operation

BRAND = '#1e6864'
BRAND_DARK = '#124c49'
BRAND_LIGHT = '#eaf5f1'
BG = '#f7faf9'
INK = '#1c3233'
MUTED = '#5a7674'
BORDER = '#d6e5e1'


class ArketypeDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Arketype — Desktop')
        self.geometry('1120x780')
        self.minsize(860, 610)
        self.configure(bg=BG)
        self.arch = {a['slug']: a for a in catalogue()}
        self.recipes = {r['id']: r for r in assemblies()}
        self.profiles = {p['slug']: p for p in use_case_profiles()}
        self.events: queue.Queue[tuple] = queue.Queue()
        self.busy = False
        self.history: list[str] = []
        self.history_index = 0
        self.current_page = ''
        self._setup_styles()
        self._make_chrome()
        self._make_home()
        self._make_catalogue()
        self._make_creator()
        self._make_ops()
        self.show_page('Home')
        self.after(120, self._poll_events)

    def _setup_styles(self):
        style = ttk.Style(self)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('.', font=('Segoe UI', 10), background=BG, foreground=INK)
        style.configure('TFrame', background=BG)
        style.configure('TLabel', background=BG, foreground=INK)
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground=BRAND_DARK)
        style.configure('Sub.TLabel', foreground=MUTED)
        style.configure('TLabelframe', background=BG, bordercolor=BORDER)
        style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'), foreground=BRAND_DARK)
        style.configure('Accent.TButton', background=BRAND, foreground='white', padding=(15, 9), font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', BRAND_DARK), ('disabled', '#a4bbb5')],
                  foreground=[('disabled', '#e1e9e5')])
        style.configure('TButton', padding=(10, 8))
        style.configure('Treeview', rowheight=28, background='white', fieldbackground='white',
                        foreground=INK, bordercolor=BORDER)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background=BRAND_LIGHT)
        style.map('Treeview', background=[('selected', BRAND)], foreground=[('selected', 'white')])

    def _make_chrome(self):
        header = tk.Frame(self, bg=BRAND_LIGHT, padx=19, pady=10, highlightthickness=1,
                          highlightbackground=BORDER)
        header.pack(fill='x')
        logo_path = ROOT / 'assets/logo-k-ui.png'
        try:
            original = tk.PhotoImage(file=str(logo_path))
            self.logo = original.subsample(2, 2)  # Compact header; source is 251x110.
            tk.Label(header, image=self.logo, bg=BRAND_LIGHT).pack(side='left', padx=(0, 20))
        except (tk.TclError, OSError):
            tk.Label(header, text='K', font=('Segoe UI', 25, 'bold'), fg=BRAND, bg=BRAND_LIGHT).pack(side='left', padx=(0, 20))
        caption = tk.Frame(header, bg=BRAND_LIGHT)
        caption.pack(side='left', fill='x', expand=True)
        tk.Label(caption, text='ARKETYPE', bg=BRAND_LIGHT, fg=BRAND_DARK,
                 font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        tk.Label(caption, text='Explore · Create · Developer Ops', bg=BRAND_LIGHT,
                 fg=MUTED, font=('Segoe UI', 10)).pack(anchor='w')
        tk.Label(header, text='LOCAL  /  NO PUBLICATION', fg=BRAND_DARK, bg=BRAND_LIGHT,
                 font=('Segoe UI', 9, 'bold')).pack(side='right', padx=8)

        area = ttk.Frame(self)
        area.pack(fill='both', expand=True)
        self.nav = tk.Frame(area, width=205, bg='#edf4f1')
        self.nav.pack(side='left', fill='y')
        self.nav.pack_propagate(False)
        self.main_area = ttk.Frame(area, padding=(24, 18, 24, 16))
        self.main_area.pack(side='left', fill='both', expand=True)
        self.nav_buttons: dict[str, tk.Button] = {}
        for page in ('Home', 'Catalogue', 'Create Kristal', 'Developer Ops'):
            btn = tk.Button(self.nav, text=page, anchor='w', font=('Segoe UI', 11),
                            relief='flat', bd=0, padx=18, pady=13, cursor='hand2',
                            bg='#edf4f1', fg=INK, activebackground=BRAND_LIGHT,
                            command=lambda item=page: self.show_page(item))
            btn.pack(fill='x', padx=8, pady=(10 if page == 'Home' else 3, 0))
            self.nav_buttons[page] = btn
        tk.Label(self.nav, text='Arketype 1.3.0\nOffline design library',
                 bg='#edf4f1', fg=MUTED, justify='left', padx=17).pack(side='bottom', anchor='w', pady=20)
        self.pages: dict[str, ttk.Frame] = {}
        self.status_var = tk.StringVar(value='Ready · no remote actions')
        ttk.Label(self, textvariable=self.status_var, anchor='w', padding=(14, 7),
                  style='Sub.TLabel').pack(fill='x', side='bottom')

    def _page(self, name, title, subtitle):
        page = ttk.Frame(self.main_area)
        self.pages[name] = page
        ttk.Label(page, text=title, style='Header.TLabel').pack(anchor='w', pady=(0, 4))
        ttk.Label(page, text=subtitle, style='Sub.TLabel').pack(anchor='w', pady=(0, 17))
        return page

    def show_page(self, name: str):
        if self.current_page:
            self.pages[self.current_page].pack_forget()
        self.current_page = name
        self.pages[name].pack(fill='both', expand=True)
        for key, btn in self.nav_buttons.items():
            active = key == name
            btn.configure(bg=BRAND if active else '#edf4f1',
                          fg='white' if active else INK,
                          font=('Segoe UI', 11, 'bold' if active else 'normal'))
        self.status_var.set(f'{name} · local only · no publication or activation')

    def _make_home(self):
        p = self._page('Home', 'Welcome to Arketype', 'One place to browse structures, create neutral Kristals, and inspect library operations.')
        ttk.Label(p, text='Choose a workflow', font=('Segoe UI', 13, 'bold')).pack(anchor='w', pady=(18, 12))
        choices = [
            ('Catalogue', 'Explore the 19 archetypes',
             'Search patterns, compare situated structures, and open the full illustrated catalogue.',
             'Explore catalogue'),
            ('Create Kristal', 'Start an independent Kristal',
             'Choose an archetype, preview an optional design-only composition, and create a blank workspace.',
             'Create Kristal'),
            ('Developer Ops', 'Inspect and verify the library',
             'Run approved local commands, unit tests, integrity checks, and HTML regeneration.',
             'Open Developer Ops'),
        ]
        for page, title, explanation, cta in choices:
            outer = tk.Frame(p, bg='white', highlightbackground=BORDER, highlightthickness=1,
                             padx=19, pady=15)
            outer.pack(fill='x', pady=7)
            tk.Label(outer, text=title, font=('Segoe UI', 13, 'bold'), fg=BRAND_DARK,
                     bg='white').pack(anchor='w')
            tk.Label(outer, text=explanation, font=('Segoe UI', 10), fg=MUTED,
                     bg='white', wraplength=680, justify='left').pack(anchor='w', pady=(5, 8))
            ttk.Button(outer, text=cta, command=lambda dest=page: self.show_page(dest),
                       style='Accent.TButton').pack(anchor='w')
        ttk.Label(p, text='All examples and composition recipes are noncanonical design guidance.',
                  style='Sub.TLabel').pack(anchor='w', pady=12)

    def _make_catalogue(self):
        p = self._page('Catalogue', 'Archetype catalogue',
                       'Browse inside Arketype, or open the full visual HTML catalogue for detailed diagrams.')
        controls = ttk.Frame(p)
        controls.pack(fill='x', pady=(0, 10))
        self.catalog_query = tk.StringVar()
        self.catalog_family = tk.StringVar(value='All families')
        self.catalog_pattern = tk.StringVar(value='All patterns')
        ttk.Label(controls, text='Search').pack(side='left')
        ttk.Entry(controls, textvariable=self.catalog_query, width=27).pack(side='left', padx=(8, 12), fill='x', expand=True)
        ttk.Combobox(controls, textvariable=self.catalog_family, state='readonly', width=17,
                     values=['All families', *sorted({a['family'] for a in self.arch.values()})]).pack(side='left', padx=(0, 9))
        ttk.Combobox(controls, textvariable=self.catalog_pattern, state='readonly', width=18,
                     values=['All patterns', *sorted({a['visual_pattern'] for a in self.arch.values()})]).pack(side='left')
        self.catalog_query.trace_add('write', lambda *_: self._refresh_catalogue())
        self.catalog_family.trace_add('write', lambda *_: self._refresh_catalogue())
        self.catalog_pattern.trace_add('write', lambda *_: self._refresh_catalogue())

        tabs = ttk.Notebook(p)
        tabs.pack(fill='both', expand=True)
        a_tab = ttk.Frame(tabs, padding=8)
        u_tab = ttk.Frame(tabs, padding=8)
        tabs.add(a_tab, text='19 Archetypes')
        tabs.add(u_tab, text='5 Use-case profiles')
        self.catalog_tabs = tabs
        self.archetype_tree = self._make_tree(a_tab, ('id', 'name', 'family', 'pattern'),
             {'id': 75, 'name': 260, 'family': 110, 'pattern': 125})
        self.profile_tree = self._make_tree(u_tab, ('id', 'name', 'archetype', 'pattern'),
             {'id': 75, 'name': 230, 'archetype': 165, 'pattern': 125})
        self.archetype_tree.bind('<<TreeviewSelect>>', self._detail_archetype)
        self.profile_tree.bind('<<TreeviewSelect>>', self._detail_profile)
        self.archetype_tree.bind('<Double-1>', lambda _: self._use_selected())
        self.catalog_details = tk.Text(p, height=8, wrap='word', relief='solid', bd=1,
                                       bg='white', font=('Segoe UI', 10), padx=12, pady=9)
        self.catalog_details.pack(fill='x', pady=(12, 6))
        self.catalog_details.configure(state='disabled')
        actions = ttk.Frame(p)
        actions.pack(fill='x')
        ttk.Button(actions, text='Open full visual catalogue', style='Accent.TButton',
                   command=self.open_visual_catalogue).pack(side='left')
        ttk.Button(actions, text='Use selected archetype', command=self._use_selected).pack(side='left', padx=10)
        ttk.Button(actions, text='Open catalogue JSON', command=lambda: self._open_file(ROOT / 'catalogue.json')).pack(side='left')
        self._refresh_catalogue()

    def _make_tree(self, parent, columns, widths):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse', height=8)
        for key in columns:
            tree.heading(key, text=key.replace('_', ' ').title())
            tree.column(key, width=widths[key], minwidth=65, stretch=key == 'name')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        return tree

    def _refresh_catalogue(self):
        query = normalized(self.catalog_query.get())
        family = self.catalog_family.get()
        pattern = self.catalog_pattern.get()
        for item in self.archetype_tree.get_children():
            self.archetype_tree.delete(item)
        for item in self.profile_tree.get_children():
            self.profile_tree.delete(item)
        for a in self.arch.values():
            haystack = normalized(' '.join(map(str, (a['name'], a['slug'], a['description'],
                       a.get('situational_schema', ''), *a.get('canonical_use_cases', [])))))
            if query and query not in haystack:
                continue
            if family != 'All families' and a['family'] != family:
                continue
            if pattern != 'All patterns' and a['visual_pattern'] != pattern:
                continue
            self.archetype_tree.insert('', 'end', iid=a['slug'], values=(a['id'], a['name'], a['family'], a['visual_pattern']))
        for profile in self.profiles.values():
            owner = self.arch[profile['primary_archetype']]
            haystack = normalized(' '.join(map(str, (profile['name'], profile['slug'],
                         profile['summary'], profile['situational_schema'], *profile['use_cases']))))
            if query and query not in haystack:
                continue
            if family != 'All families' and owner['family'] != family:
                continue
            if pattern != 'All patterns' and profile['visual_pattern'] != pattern:
                continue
            self.profile_tree.insert('', 'end', iid=profile['slug'], values=(
                profile['id'], profile['name'], profile['primary_archetype'], profile['visual_pattern']))
        self._set_catalogue_detail('Select an archetype or use-case profile for its description and design boundaries.')

    def _set_catalogue_detail(self, value):
        self.catalog_details.configure(state='normal')
        self.catalog_details.delete('1.0', 'end')
        self.catalog_details.insert('1.0', value)
        self.catalog_details.configure(state='disabled')

    def _detail_archetype(self, _event=None):
        selected = self.archetype_tree.selection()
        if selected:
            self._set_catalogue_detail(render_archetype(self.arch[selected[0]]))

    def _detail_profile(self, _event=None):
        selected = self.profile_tree.selection()
        if selected:
            self._set_catalogue_detail(render_profile(self.profiles[selected[0]]))

    def _use_selected(self):
        # Selection is scoped to the currently visible catalogue tab, not
        # whichever tree was selected most recently.
        if self.catalog_tabs.index(self.catalog_tabs.select()) == 1:
            selected = self.profile_tree.selection()
            if selected:
                owner = self.profiles[selected[0]]
                self.selected_type.set(owner['primary_archetype'])
                self.selected_recipe.set(owner['assemblage_reference'])
                self._update_creator_type(update_recipe=False)
                self.show_page('Create Kristal')
                return
        else:
            selected = self.archetype_tree.selection()
            if selected:
                self.selected_type.set(selected[0])
                self._update_creator_type()
                self.show_page('Create Kristal')
                return
        messagebox.showinfo('Select an archetype', 'Select an archetype or use-case profile first.')

    def _make_creator(self):
        p = self._page('Create Kristal', 'Create a neutral Kristal',
                       'Design-only creation using the bundled Authoring Kit. Preview first; nothing is published.')
        frm = ttk.Frame(p)
        frm.pack(fill='x', pady=5)
        frm.columnconfigure(1, weight=1)
        self.selected_type = tk.StringVar(value=next(iter(self.arch)))
        self.selected_recipe = tk.StringVar(value='None')
        self.new_slug = tk.StringVar()
        self.new_title = tk.StringVar()
        self.parent_folder = tk.StringVar()
        labels = ('Primary archetype', 'Optional assembly', 'Kristal slug', 'Kristal title', 'Parent directory')
        for row, title in enumerate(labels):
            ttk.Label(frm, text=title).grid(row=row, column=0, sticky='w', padx=(0, 18), pady=10)
        # Two-part description selected by human-readable display and stable slug.
        self.type_display = tk.StringVar()
        self.type_labels = {f"{a['id']}  ·  {a['name']}": a['slug'] for a in self.arch.values()}
        self.inverse_type_labels = {v: k for k, v in self.type_labels.items()}
        self.type_display.set(self.inverse_type_labels[self.selected_type.get()])
        combo = ttk.Combobox(frm, textvariable=self.type_display, state='readonly',
                             values=list(self.type_labels), width=55)
        combo.grid(row=0, column=1, sticky='ew', pady=5)
        combo.bind('<<ComboboxSelected>>', self._on_type_change)
        self.recipe_display = tk.StringVar(value='None')
        self.assembly_labels: dict[str, str] = {}
        self.recipe_widget = ttk.Combobox(frm, textvariable=self.recipe_display, state='readonly')
        self.recipe_widget.grid(row=1, column=1, sticky='ew', pady=5)
        self.recipe_widget.bind('<<ComboboxSelected>>', self._on_recipe_change)
        ttk.Entry(frm, textvariable=self.new_slug).grid(row=2, column=1, sticky='ew', pady=5)
        ttk.Entry(frm, textvariable=self.new_title).grid(row=3, column=1, sticky='ew', pady=5)
        p_frame = ttk.Frame(frm)
        p_frame.grid(row=4, column=1, sticky='ew', pady=5)
        p_frame.columnconfigure(0, weight=1)
        ttk.Entry(p_frame, textvariable=self.parent_folder).grid(row=0, column=0, sticky='ew')
        ttk.Button(p_frame, text='Browse…', command=self._choose_folder).grid(row=0, column=1, padx=(8, 0))
        self.creator_description = tk.Text(p, height=10, wrap='word', relief='solid',
                                           bg='white', font=('Segoe UI', 10), padx=12, pady=10)
        self.creator_description.pack(fill='both', expand=True, pady=(12, 8))
        self.creator_description.configure(state='disabled')
        buttons = ttk.Frame(p)
        buttons.pack(fill='x')
        ttk.Button(buttons, text='Preview (no files written)', command=lambda: self._submit_create(True)).pack(side='left', padx=(0, 10))
        self.create_button = ttk.Button(buttons, text='Create Kristal', style='Accent.TButton',
                                        command=lambda: self._submit_create(False))
        self.create_button.pack(side='left')
        ttk.Label(buttons, text='New state_ref · Empty canon · No publication',
                  style='Sub.TLabel').pack(side='right')
        self._update_creator_type()

    def _choose_folder(self):
        path = filedialog.askdirectory(title='Choose an existing parent directory')
        if path:
            self.parent_folder.set(path)

    def _on_type_change(self, event=None):
        self.selected_type.set(self.type_labels[self.type_display.get()])
        self._update_creator_type()

    def _update_creator_type(self, update_recipe=True):
        typ = self.selected_type.get()
        self.type_display.set(self.inverse_type_labels[typ])
        self.assembly_labels = {'None': 'None'}
        for rec in self.recipes.values():
            if rec['primary_archetype'] == typ:
                self.assembly_labels[f"{rec['title']}  [{rec['id']}]"] = rec['id']
        self.recipe_widget.configure(values=list(self.assembly_labels))
        if update_recipe:
            self.selected_recipe.set('None')
        selected = next((k for k, v in self.assembly_labels.items() if v == self.selected_recipe.get()), 'None')
        self.recipe_display.set(selected)
        self._update_creator_description()

    def _on_recipe_change(self, event=None):
        self.selected_recipe.set(self.assembly_labels[self.recipe_display.get()])
        self._update_creator_description()

    def _update_creator_description(self):
        desc = render_archetype(self.arch[self.selected_type.get()])
        recipe = self.recipes.get(self.selected_recipe.get())
        if recipe:
            desc += f"\n\nAssembly: {recipe['title']}\n" + '\n'.join(
                f"  + {c['archetype']} [{c['relation']}]" for c in recipe['components'])
            desc += '\n\nDesign-only proposal. No canonical states will be merged.'
        self.creator_description.configure(state='normal')
        self.creator_description.delete('1.0', 'end')
        self.creator_description.insert('1.0', desc)
        self.creator_description.configure(state='disabled')

    def _submit_create(self, dry_run: bool):
        try:
            typ = self.selected_type.get()
            slug = self.new_slug.get().strip()
            title = self.new_title.get().strip()
            folder = self.parent_folder.get().strip()
            recipe = self.selected_recipe.get()
            if recipe == 'None':
                recipe = None
            if not folder:
                raise ValueError('Select an existing parent directory.')
            if dry_run:
                result = create(typ, slug, title, folder, recipe=recipe, dry_run=True)
                messagebox.showinfo('Preview — No files written', json.dumps(result, ensure_ascii=False, indent=2))
                return
            if self.busy:
                return
            if not messagebox.askyesno('Confirm local creation',
                f'Create a neutral Kristal named "{title}" in:\n{folder}/{slug}\n\nNo domain content is published.'):
                return
            self._start_job('create', (typ, slug, title, folder, recipe))
        except Exception as exc:
            messagebox.showerror('Arketype — Creation issue', str(exc))

    def _make_ops(self):
        p = self._page('Developer Ops', 'Developer Ops console',
                       'Local allowlisted commands only. No shell execution, remote deployment, or activation.')
        actions = ttk.Frame(p)
        actions.pack(fill='x', pady=(0, 12))
        for title, cmd in (('Status', 'status'), ('Validate', 'validate'),
                           ('Check Local Kit', 'validate --check-kit'), ('Run tests', 'test'),
                           ('Verify inventory', 'inventory'), ('Regenerate HTML', 'build-html')):
            ttk.Button(actions, text=title, command=lambda c=cmd: self._run_console(c)).pack(side='left', padx=(0, 7))
        self.ops_output = scrolledtext.ScrolledText(p, wrap='word', font=('Consolas', 10),
                  bg='#112b2b', fg='#e4f4ed', insertbackground='white', relief='flat',
                  padx=14, pady=13)
        self.ops_output.pack(fill='both', expand=True)
        self.ops_output.insert('end', 'Arketype Developer Ops · Type help for available commands.\n'
                                      'No remote publication or activation is supported.\n\n')
        self.ops_output.configure(state='disabled')
        command_frame = ttk.Frame(p)
        command_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(command_frame, text='arketype >').pack(side='left')
        self.ops_input = tk.StringVar()
        inp = ttk.Entry(command_frame, textvariable=self.ops_input)
        inp.pack(side='left', fill='x', expand=True, padx=10)
        inp.bind('<Return>', lambda event: self._run_console())
        inp.bind('<Up>', self._history_up)
        inp.bind('<Down>', self._history_down)
        self.ops_run_button = ttk.Button(command_frame, text='Run', style='Accent.TButton',
                                         command=self._run_console)
        self.ops_run_button.pack(side='left')
        ttk.Button(command_frame, text='Clear', command=self._clear_console).pack(side='left', padx=(8, 0))

    def _history_up(self, event):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            self.ops_input.set(self.history[self.history_index])
        return 'break'

    def _history_down(self, event):
        if self.history:
            self.history_index = min(len(self.history), self.history_index + 1)
            self.ops_input.set(self.history[self.history_index] if self.history_index < len(self.history) else '')
        return 'break'

    def _clear_console(self):
        self.ops_output.configure(state='normal')
        self.ops_output.delete('1.0', 'end')
        self.ops_output.configure(state='disabled')

    def _append_console(self, text):
        self.ops_output.configure(state='normal')
        self.ops_output.insert('end', text + '\n')
        self.ops_output.see('end')
        self.ops_output.configure(state='disabled')

    def _run_console(self, value=None):
        command = (value if value is not None else self.ops_input.get()).strip()
        if not command:
            return
        self.ops_input.set('')
        self.history.append(command)
        self.history_index = len(self.history)
        self._append_console('> ' + command)
        try:
            op = parse_operation(command)
            if op.kind == 'clear':
                self._clear_console()
            elif op.kind == 'open':
                self.open_visual_catalogue()
                self._append_console('Opened the offline catalogue in your browser.\n')
            else:
                if self.busy:
                    self._append_console('An operation is already running. Please wait.\n')
                    return
                self._start_job('operation', op)
        except OperationError as exc:
            self._append_console('ERROR: ' + str(exc) + '\n')

    def _start_job(self, mode, payload):
        self.busy = True
        self.ops_run_button.configure(state='disabled')
        self.create_button.configure(state='disabled')
        self.status_var.set('Working locally…')
        def work():
            try:
                if mode == 'create':
                    typ, slug, title, folder, recipe = payload
                    result = create(typ, slug, title, folder, recipe=recipe)
                    self.events.put(('create', 0, str(result)))
                else:
                    code, output = run_operation(payload)
                    self.events.put(('operation', code, output))
            except Exception as exc:
                self.events.put((mode, 1, str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def _poll_events(self):
        try:
            while True:
                mode, code, output = self.events.get_nowait()
                self.busy = False
                self.ops_run_button.configure(state='normal')
                self.create_button.configure(state='normal')
                self.status_var.set('Ready · local only · no publication or activation')
                if mode == 'create':
                    if code == 0:
                        messagebox.showinfo('Neutral workspace created',
                            'Created and checked:\n' + output + '\n\nNo domain assertions or publication.')
                        self._append_console('Created local workspace: ' + output)
                    else:
                        messagebox.showerror('Creation failed', output)
                else:
                    self._append_console(output + f'\n[Exit code: {code}]\n')
                    if code != 0:
                        self.status_var.set('Last operation reported an error — see Developer Ops')
        except queue.Empty:
            pass
        self.after(120, self._poll_events)

    def open_visual_catalogue(self):
        self._open_file(ROOT / 'catalogue' / 'index.html')

    def _open_file(self, path: Path):
        if not path.is_file():
            messagebox.showerror('File not found', str(path))
            return
        webbrowser.open(path.resolve().as_uri())


def main():
    app = ArketypeDesktop()
    app.mainloop()


if __name__ == '__main__':
    main()
