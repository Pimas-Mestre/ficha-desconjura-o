import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import math
import os
import webbrowser

# ============================================================
# DESCONJURAÇÃO - GERADOR DE FICHA
# Baseado no PDF "DESCONJURAÇÃO" enviado pelo usuário.
# ============================================================

# Opcional: coloque uma URL pública de um design/banner do Canva na variável
# de ambiente DESCONJURACAO_CANVA_URL. O programa não depende do Canva para rodar.
CANVA_PUBLIC_URL = os.getenv("DESCONJURACAO_CANVA_URL", "https://www.canva.com/")

ATTRS = [
    ("FOR", "Força"),
    ("CON", "Constituição"),
    ("TAM", "Tamanho"),
    ("DES", "Destreza"),
    ("APA", "Aparência"),
    ("INT", "Inteligência"),
    ("POD", "Poder"),
    ("EDU", "Educação"),
]

SKILLS = {
    "Acrobacia": 4,
    "Antropologia": 1,
    "Armas (Pistolas)": 4,
    "Armas (Rifles/Espingardas)": 5,
    "Armas (Arcos/Bestas)": 3,
    "Arqueologia": 1,
    "Arremessar": 4,
    "Arte e Ofício": 1,
    "Avaliação": 1,
    "Cavalgar": 1,
    "Charme": 3,
    "Chaveiro": 1,
    "Ciência (Biologia)": 1,
    "Ciência (Forense)": 1,
    "Ciência (Farmácia)": 1,
    "Ciência (Química)": 1,
    "Conhecimento": 1,
    "Consertos Elétricos": 2,
    "Consertos Mecânicos": 2,
    "Contabilidade": 1,
    "Demolições": 1,
    "Direito": 1,
    "Dirigir": 4,
    "Disfarce": 1,
    "Eletrônica": 1,
    "Encontrar": 5,
    "Escutar": 4,
    "Esquivar": "DES/2",
    "Furtividade": 4,
    "Hipnose": 1,
    "História": 1,
    "Intimidação": 3,
    "Lábia": 1,
    "Leitura Labial": 1,
    "Língua (Nativa)": "EDU",
    "Língua (Outra)": 1,
    "Lutar (Brigar)": 5,
    "Medicina": 1,
    "Mergulho": 1,
    "Mundo Natural": 2,
    "Natação": 2,
    "Navegação": 2,
    "Ocultismo": 2,
    "Operar Maquinário": 1,
    "Persuasão": 2,
    "Pilotar (Aeronave)": 1,
    "Pilotar (Barco)": 1,
    "Prestidigitação": 2,
    "Primeiros Socorros": 6,
    "Psicanálise": 1,
    "Psicologia": 2,
    "Rastrear": 2,
    "Sobrevivência": 2,
    "Treinar Animais": 1,
    "Usar Bibliotecas": 4,
    "Usar Computadores": 4,
}

# Ocupações transcritas/resumidas do PDF.
# Entradas como "QUALQUER" significam que o jogador escolhe a perícia.
OCCUPATIONS = {
    "CONTADOR": ["Contabilidade", "Direito", "Usar Bibliotecas", "Escutar", "Persuasão", "Encontrar", "QUALQUER", "QUALQUER"],
    "ACROBATA": ["Acrobacia", "Esquivar", "Arremessar", "Encontrar", "Natação", "QUALQUER", "QUALQUER", "QUALQUER"],
    "ATOR DE TEATRO": ["Arte e Ofício (Atuação)", "Disfarce", "Lutar (Brigar)", "História", "Psicologia", "SOCIAL", "SOCIAL", "QUALQUER"],
    "ATOR DE CINEMA": ["Arte e Ofício (Atuação)", "Disfarce", "Dirigir", "Psicologia", "SOCIAL", "SOCIAL", "QUALQUER", "QUALQUER"],
    "DETETIVE": ["Lutar (Brigar)", "Armas (Pistolas)", "Direito", "Usar Bibliotecas", "Psicologia", "Furtividade", "Rastrear", "SOCIAL"],
    "TREINADOR DE ANIMAIS": ["Acrobacia", "Escutar", "Mundo Natural", "Psicologia", "Ciência (Biologia)", "Furtividade", "Rastrear", "Treinar Animais"],
    "ANTIQUÁRIO": ["Avaliação", "Arte e Ofício", "História", "Usar Bibliotecas", "Língua (Outra)", "Encontrar", "SOCIAL", "QUALQUER"],
    "ARQUEÓLOGO": ["Avaliação", "Arqueologia", "História", "Língua (Outra)", "Usar Bibliotecas", "Encontrar", "Consertos Mecânicos", "Navegação"],
    "ARQUITETO": ["Contabilidade", "Arte e Ofício (Desenho Técnico)", "Direito", "Língua (Nativa)", "Persuasão", "Psicologia", "Ciência (Matemática)", "Usar Bibliotecas"],
    "ARTISTA VISUAL": ["Arte e Ofício", "Língua (Outra)", "Psicologia", "Encontrar", "Mundo Natural", "SOCIAL", "QUALQUER", "QUALQUER"],
    "ATLETA": ["Acrobacia", "Lutar (Brigar)", "Cavalgar", "Natação", "Arremessar", "SOCIAL", "QUALQUER", "QUALQUER"],
    "AUTOR": ["Arte e Ofício (Literatura)", "História", "Usar Bibliotecas", "Língua (Outra)", "Língua (Nativa)", "Psicologia", "Mundo Natural", "QUALQUER"],
    "BARTENDER": ["Contabilidade", "Lutar (Brigar)", "Escutar", "Psicologia", "Encontrar", "SOCIAL", "SOCIAL", "QUALQUER"],
    "CAÇADOR": ["Armas (Pistolas)", "Mundo Natural", "Navegação", "Furtividade", "Rastrear", "Escutar", "Língua (Outra)", "Ciência (Biologia)"],
    "BOXER/WRESTLER": ["Esquivar", "Lutar (Brigar)", "Intimidação", "Acrobacia", "Psicologia", "Encontrar", "QUALQUER", "QUALQUER"],
    "MORDOMO": ["Arte e Ofício", "Primeiros Socorros", "Escutar", "Língua (Outra)", "Psicologia", "Encontrar", "Avaliação", "QUALQUER"],
    "MEMBRO DO CLERO": ["Contabilidade", "História", "Usar Bibliotecas", "Escutar", "Língua (Outra)", "Psicologia", "SOCIAL", "QUALQUER"],
    "PROGRAMADOR/TÉCNICO DE PC": ["Usar Computadores", "Consertos Elétricos", "Eletrônica", "Usar Bibliotecas", "Ciência (Matemática)", "Encontrar", "QUALQUER", "QUALQUER"],
    "HACKER": ["Usar Computadores", "Consertos Elétricos", "Usar Bibliotecas", "Eletrônica", "Encontrar", "SOCIAL", "QUALQUER", "QUALQUER"],
    "COWBOY": ["Esquivar", "Acrobacia", "Cavalgar", "Sobrevivência", "Arremessar", "Rastrear", "Lutar (Brigar)", "Primeiros Socorros"],
    "ARTESÃO": ["Contabilidade", "Arte e Ofício", "Consertos Mecânicos", "Mundo Natural", "Encontrar", "QUALQUER", "QUALQUER", "QUALQUER"],
    "ASSASSINO": ["Disfarce", "Consertos Elétricos", "Lutar (Brigar)", "Armas (Pistolas)", "Chaveiro", "Consertos Mecânicos", "Furtividade", "Psicologia"],
    "LADRÃO DE BANCO": ["Dirigir", "Lutar (Brigar)", "Armas (Pistolas)", "Intimidação", "Chaveiro", "Operar Maquinário", "Consertos Mecânicos", "QUALQUER"],
    "CRIMINOSO": ["Avaliação", "Acrobacia", "Escutar", "Chaveiro", "Prestidigitação", "Furtividade", "Encontrar", "Consertos Mecânicos"],
    "VIGARISTA": ["Avaliação", "Arte e Ofício (Atuação)", "Escutar", "Psicologia", "Prestidigitação", "Direito", "SOCIAL", "SOCIAL"],
    "FALSIFICADOR": ["Contabilidade", "Avaliação", "Arte e Ofício (Falsificação)", "História", "Usar Bibliotecas", "Encontrar", "Prestidigitação", "QUALQUER"],
    "CONTRABANDISTA": ["Armas (Pistolas)", "Escutar", "Navegação", "Psicologia", "Prestidigitação", "Encontrar", "Dirigir", "SOCIAL"],
    "CULTISTA": ["Contabilidade", "Psicologia", "Encontrar", "SOCIAL", "SOCIAL", "QUALQUER", "QUALQUER", "QUALQUER"],
    "DESIGNER": ["Contabilidade", "Arte e Ofício (Fotografia)", "Arte e Ofício", "Consertos Mecânicos", "Psicologia", "Encontrar", "Usar Computadores", "QUALQUER"],
    "DILETTANTE": ["Arte e Ofício", "Armas (Pistolas)", "Língua (Outra)", "Cavalgar", "SOCIAL", "QUALQUER", "QUALQUER", "QUALQUER"],
    "MERGULHADOR": ["Mergulho", "Primeiros Socorros", "Consertos Mecânicos", "Pilotar (Barco)", "Ciência (Biologia)", "Encontrar", "Natação", "QUALQUER"],
    "MÉDICO": ["Primeiros Socorros", "Medicina", "Língua (Latim)", "Psicologia", "Ciência (Biologia)", "Ciência (Farmácia)", "QUALQUER", "QUALQUER"],
    "MOTORISTA": ["Contabilidade", "Dirigir", "Escutar", "Consertos Mecânicos", "Navegação", "Psicologia", "SOCIAL", "QUALQUER"],
    "POLÍTICO": ["Charme", "História", "Intimidação", "Lábia", "Escutar", "Persuasão", "Língua (Nativa)", "Psicologia"],
    "ENGENHEIRO": ["Arte e Ofício (Desenho Técnico)", "Consertos Elétricos", "Consertos Mecânicos", "Usar Bibliotecas", "Operar Maquinário", "Ciência (Engenharia)", "Ciência (Física)", "QUALQUER"],
    "FAZENDEIRO": ["Arte e Ofício (Fazenda)", "Dirigir", "Consertos Mecânicos", "Mundo Natural", "Operar Maquinário", "Rastrear", "SOCIAL", "QUALQUER"],
    "AGENTE FEDERAL": ["Dirigir", "Lutar (Brigar)", "Armas (Pistolas)", "Direito", "Persuasão", "Furtividade", "Encontrar", "QUALQUER"],
    "BOMBEIRO": ["Acrobacia", "Esquivar", "Dirigir", "Primeiros Socorros", "Consertos Mecânicos", "Operar Maquinário", "Arremessar", "QUALQUER"],
    "CIRURGIÃO FORENSE": ["Língua (Latim)", "Usar Bibliotecas", "Medicina", "Persuasão", "Ciência (Biologia)", "Ciência (Forense)", "Ciência (Farmácia)", "Encontrar"],
    "APOSTADOR": ["Contabilidade", "Arte e Ofício (Atuação)", "Escutar", "Psicologia", "Prestidigitação", "Encontrar", "SOCIAL", "SOCIAL"],
    "GANGSTER": ["Dirigir", "Lutar (Brigar)", "Armas (Pistolas)", "Psicologia", "SOCIAL", "SOCIAL", "QUALQUER", "QUALQUER"],
    "NÔMADE": ["Arte e Ofício", "Acrobacia", "Escutar", "Chaveiro", "Navegação", "Furtividade", "QUALQUER", "QUALQUER"],
    "JORNALISTA INVESTIGATIVO": ["Arte e Ofício (Fotografia)", "SOCIAL", "História", "Usar Bibliotecas", "Língua (Nativa)", "Psicologia", "QUALQUER", "QUALQUER"],
    "REPORTER": ["Arte e Ofício (Atuação)", "História", "Escutar", "Língua (Nativa)", "SOCIAL", "Psicologia", "Furtividade", "Encontrar"],
    "JUIZ": ["História", "Intimidação", "Direito", "Usar Bibliotecas", "Escutar", "Língua (Nativa)", "Persuasão", "Psicologia"],
    "ADVOGADO": ["Contabilidade", "Direito", "Usar Bibliotecas", "SOCIAL", "SOCIAL", "Psicologia", "QUALQUER", "QUALQUER"],
    "BIBLIOTECÁRIO": ["Contabilidade", "Usar Bibliotecas", "Língua (Outra)", "Língua (Nativa)", "QUALQUER", "QUALQUER", "QUALQUER", "QUALQUER"],
    "MECÂNICO": ["Arte e Ofício", "Acrobacia", "Dirigir", "Consertos Elétricos", "Consertos Mecânicos", "Operar Maquinário", "QUALQUER", "QUALQUER"],
    "OFICIAL MILITAR": ["Contabilidade", "Armas (Pistolas)", "Navegação", "Primeiros Socorros", "SOCIAL", "SOCIAL", "Psicologia", "QUALQUER"],
    "MISSIONÁRIO": ["Arte e Ofício", "Primeiros Socorros", "Consertos Mecânicos", "Medicina", "Mundo Natural", "SOCIAL", "QUALQUER", "QUALQUER"],
    "ALPINISTA": ["Acrobacia", "Primeiros Socorros", "Escutar", "Navegação", "Língua (Outra)", "Sobrevivência", "Rastrear", "QUALQUER"],
    "CURADOR DE MUSEU": ["Contabilidade", "Avaliação", "Arqueologia", "História", "Usar Bibliotecas", "Língua (Outra)", "Encontrar", "QUALQUER"],
    "MÚSICO": ["Arte e Ofício (Instrumento)", "SOCIAL", "Psicologia", "Escutar", "QUALQUER", "QUALQUER", "QUALQUER", "QUALQUER"],
    "ENFERMEIRA": ["Primeiros Socorros", "Escutar", "Medicina", "SOCIAL", "Psicologia", "Ciência (Biologia)", "Encontrar", "Ciência (Química)"],
    "FARMACÊUTICO": ["Contabilidade", "Primeiros Socorros", "Língua (Latim)", "Usar Bibliotecas", "SOCIAL", "Psicologia", "Ciência (Farmácia)", "Ciência (Química)"],
    "FOTÓGRAFO": ["Arte e Ofício (Fotografia)", "SOCIAL", "Psicologia", "Furtividade", "Encontrar", "QUALQUER", "QUALQUER", "QUALQUER"],
    "PILOTO": ["Consertos Elétricos", "Consertos Mecânicos", "Navegação", "Operar Maquinário", "Pilotar (Aeronave)", "Ciência (Astronomia)", "QUALQUER", "QUALQUER"],
    "DETETIVE DA POLÍCIA": ["Disfarce", "Armas (Pistolas)", "Direito", "Escutar", "SOCIAL", "Psicologia", "Encontrar", "QUALQUER"],
    "OFICIAL DA POLÍCIA": ["Lutar (Brigar)", "Armas (Pistolas)", "Primeiros Socorros", "SOCIAL", "Direito", "Psicologia", "Encontrar", "Dirigir"],
    "PROFESSOR": ["Usar Bibliotecas", "Língua (Outra)", "Língua (Nativa)", "Psicologia", "QUALQUER", "QUALQUER", "QUALQUER", "QUALQUER"],
    "GARIMPEIRO": ["Acrobacia", "Primeiros Socorros", "História", "Consertos Mecânicos", "Navegação", "Ciência (Geologia)", "Encontrar", "QUALQUER"],
    "PSIQUIATRA": ["Língua (Outra)", "Escutar", "Medicina", "Persuasão", "Psicanálise", "Psicologia", "Ciência (Biologia)", "Ciência (Química)"],
    "PSICÓLOGO": ["Contabilidade", "Usar Bibliotecas", "Escutar", "Persuasão", "Psicanálise", "Psicologia", "QUALQUER", "QUALQUER"],
    "PESQUISADOR": ["História", "Usar Bibliotecas", "SOCIAL", "Língua (Outra)", "Encontrar", "QUALQUER", "QUALQUER", "QUALQUER"],
    "MARINHEIRO": ["Consertos Mecânicos", "Lutar (Brigar)", "Armas (Pistolas)", "Primeiros Socorros", "Navegação", "Pilotar (Barco)", "Sobrevivência", "Natação"],
    "VENDEDOR": ["Contabilidade", "SOCIAL", "SOCIAL", "Dirigir", "Escutar", "Psicologia", "Furtividade", "QUALQUER"],
    "CIENTISTA": ["Ciência (Biologia)", "Ciência (Forense)", "Ciência (Química)", "Usar Bibliotecas", "Língua (Outra)", "Língua (Nativa)", "Encontrar", "SOCIAL"],
    "SECRETÁRIO": ["Contabilidade", "Arte e Ofício (Digitação)", "SOCIAL", "SOCIAL", "Língua (Nativa)", "Usar Bibliotecas", "Psicologia", "QUALQUER"],
    "LOJISTA": ["Contabilidade", "SOCIAL", "SOCIAL", "Consertos Elétricos", "Escutar", "Consertos Mecânicos", "Psicologia", "Encontrar"],
    "SOLDADO": ["Acrobacia", "Esquivar", "Lutar (Brigar)", "Armas (Pistolas)", "Furtividade", "Sobrevivência", "Primeiros Socorros", "Consertos Mecânicos"],
    "ESPIÃO": ["Disfarce", "Armas (Pistolas)", "Escutar", "Língua (Outra)", "SOCIAL", "Psicologia", "Prestidigitação", "Furtividade"],
    "ESTUDANTE": ["Língua (Nativa)", "Usar Bibliotecas", "Escutar", "QUALQUER", "QUALQUER", "QUALQUER", "QUALQUER", "QUALQUER"],
    "DUBLÊ": ["Acrobacia", "Esquivar", "Consertos Mecânicos", "Lutar (Brigar)", "Primeiros Socorros", "Natação", "Dirigir", "Cavalgar"],
    "MEMBRO DE TRIBO": ["Acrobacia", "Lutar (Brigar)", "Escutar", "Mundo Natural", "Encontrar", "Natação", "Sobrevivência", "QUALQUER"],
    "AGENTE FUNERÁRIO": ["Contabilidade", "Dirigir", "SOCIAL", "História", "Psicologia", "Ciência (Biologia)", "Ciência (Química)", "QUALQUER"],
    "ATIVISTA": ["Contabilidade", "SOCIAL", "SOCIAL", "Lutar (Brigar)", "Direito", "Escutar", "Operar Maquinário", "Psicologia"],
    "GARÇOM": ["Contabilidade", "Arte e Ofício", "Esquivar", "Escutar", "SOCIAL", "SOCIAL", "Psicologia", "QUALQUER"],
    "ANDARILHO": ["Acrobacia", "Escutar", "Furtividade", "SOCIAL", "Navegação", "QUALQUER", "QUALQUER", "QUALQUER"],
    "FANÁTICO": ["Furtividade", "História", "SOCIAL", "SOCIAL", "Psicologia", "QUALQUER", "QUALQUER", "QUALQUER"],
    "PARAPSICÓLOGO": ["Antropologia", "Arte e Ofício (Fotografia)", "História", "Usar Bibliotecas", "Língua (Outra)", "Psicologia", "QUALQUER", "QUALQUER"],
    "PROFISSIONAL DE ENTRETENIMENTO": ["Arte e Ofício (Atuação)", "Disfarce", "Escutar", "SOCIAL", "SOCIAL", "Psicologia", "QUALQUER", "QUALQUER"],
}

SOCIAL = ["Charme", "Lábia", "Intimidação", "Persuasão"]
CHOICE = [s for s in SKILLS if isinstance(SKILLS[s], (int, str))]

def roll(n, sides):
    return sum(random.randint(1, sides) for _ in range(n))

def skill_base(name, attrs):
    if name == "Esquivar":
        return attrs["DES"] // 2
    if name == "Língua (Nativa)":
        return attrs["EDU"]
    return SKILLS.get(name, 1) if isinstance(SKILLS.get(name, 1), int) else 1

# Tabela de testes da ficha:
# Valor da habilidade -> Normal, Bom, Extremo.
# Um resultado 1 sempre é Fracasso Extremo.
ROLL_TABLE = {
    1:  (20, None, None),
    2:  (19, 20, None),
    3:  (18, 20, None),
    4:  (17, 19, None),
    5:  (16, 19, 20),
    6:  (15, 18, 20),
    7:  (14, 18, 20),
    8:  (13, 17, 20),
    9:  (12, 17, 20),
    10: (11, 16, 19),
    11: (10, 16, 19),
    12: (9, 15, 19),
    13: (8, 15, 19),
    14: (7, 14, 19),
    15: (6, 14, 18),
    16: (5, 13, 18),
    17: (4, 13, 18),
    18: (3, 12, 18),
    19: (2, 12, 18),
    20: (1, 11, 17),
}

DICE_VALUES = [20]  # Os testes do sistema usam d20; o rolador livre continua aceitando outros dados.

def get_roll_thresholds(value):
    """Retorna (Normal, Bom, Extremo) para um valor de habilidade 1-20."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = 1
    value = max(1, min(20, value))
    return ROLL_TABLE[value]

def classify_roll(value, result):
    """
    Classifica uma rolagem usando a tabela:
    1 = Fracasso Extremo;
    abaixo de Normal = Fracasso;
    Normal até antes de Bom = Normal;
    Bom até antes de Extremo = Bom;
    Extremo em diante = Extremo.
    """
    normal, bom, extremo = get_roll_thresholds(value)

    if result == 1:
        return "Fracasso extremo", "fail_extreme"
    if result < normal:
        return "Fracasso", "fail"
    if extremo is not None and result >= extremo:
        return "Extremo", "extreme"
    if bom is not None and result >= bom:
        return "Bom", "good"
    return "Normal", "normal"


def damage_bonus_and_body(for_, tam):
    total = for_ + tam
    if total <= 12: return "-2", -2
    if total <= 16: return "-1", -1
    if total <= 24: return "0", 0
    if total <= 32: return "+1d4", 1
    if total <= 40: return "+1d6", 2
    if total <= 56: return "+2d6", 3
    if total <= 72: return "+3d6", 4
    if total <= 88: return "+4d6", 5
    extra = 5 + ((total - 89) // 16)
    dice = extra
    return f"+{dice}d6", extra

def calc_mov(for_, des, tam):
    if for_ > tam and des > tam:
        return 9
    if for_ >= tam or des >= tam:
        return 8
    return 7

def roll_attributes(mode):
    # Regra de criação de personagem do PDF:
    # campanha mediana = 4d6, descartando o menor dado, para cada atributo.
    if mode == "Fácil":
        return [roll(2, 6) + 6 for _ in ATTRS]
    if mode == "Médio":
        return [sum(sorted([random.randint(1,6) for _ in range(4)])[1:]) for _ in ATTRS]
    if mode == "Difícil":
        return [roll(3, 6) for _ in ATTRS]
    values = [8,10,10,10,12,12,14,16]
    random.shuffle(values)
    return values


class App:
    NEX_VALUES = list(range(5, 81, 5))

    def __init__(self, root):
        self.root = root
        self.root.title("Desconjuração — Criador de Ficha")
        self.root.geometry("1280x900")
        self.root.minsize(1050, 720)

        self.vars = {}
        self.skill_vars = {}
        self.attr_roll_labels = {}
        self.skill_roll_labels = {}
        self.roll_mode_var = tk.StringVar(value="Normal")
        self.dice_var = tk.StringVar(value="d20")
        self.nex_var = tk.IntVar(value=5)
        self.archetype_var = tk.StringVar(value="Ainda não escolhido")
        self.epic_group_var = tk.StringVar(value="Nenhum")
        self.history = []

        # Escolhas numéricas da progressão.
        self.progress_choices = {
            "attr25": tk.StringVar(value="Nenhum"),
            "attr30": tk.StringVar(value="Nenhum"),
            "attr40": tk.StringVar(value="Nenhum"),
            "attr45a": tk.StringVar(value="Nenhum"),
            "attr45b": tk.StringVar(value="Nenhum"),
            "group_attr1": tk.StringVar(value="Nenhum"),
            "group_attr2": tk.StringVar(value="Nenhum"),
            "group_attr3": tk.StringVar(value="Nenhum"),
            "swap40a": tk.StringVar(value="Nenhum"),
            "swap40b": tk.StringVar(value="Nenhum"),
            "swap45a": tk.StringVar(value="Nenhum"),
            "swap45b": tk.StringVar(value="Nenhum"),
        }

        self.base_max = {"vida": 0, "sanidade": 0, "ocultismo": 0}
        self.current_status = {"vida": 0, "sanidade": 0, "ocultismo": 0}
        self.status_vars = {}
        self.status_bars = {}
        self.status_max_labels = {}

        self.setup_theme()
        self.build_ui()
        self.update_progression()
        self.update_status()

    # ------------------------------------------------------------
    # Barra de status
    # ------------------------------------------------------------
    def build_status_bar(self):
        outer = ttk.LabelFrame(self.root, text="STATUS")
        outer.pack(fill="x", padx=8, pady=(8, 0))

        for col, (key, label) in enumerate([
            ("vida", "VIDA"),
            ("sanidade", "SANIDADE"),
            ("ocultismo", "PONTOS DE OCULTISMO"),
        ]):
            frame = ttk.Frame(outer)
            frame.grid(row=0, column=col, sticky="ew", padx=10, pady=7)
            outer.columnconfigure(col, weight=1)

            ttk.Label(frame, text=label, font=("Arial", 9, "bold")).grid(
                row=0, column=0, sticky="w"
            )
            var = tk.IntVar(value=0)
            self.status_vars[key] = var
            spin = ttk.Spinbox(
                frame, from_=0, to=9999, width=6,
                textvariable=var, command=lambda k=key: self.status_changed(k)
            )
            spin.grid(row=0, column=1, padx=7)
            spin.bind("<FocusOut>", lambda e, k=key: self.status_changed(k))
            spin.bind("<Return>", lambda e, k=key: self.status_changed(k))

            bar = ttk.Progressbar(
                frame, orient="horizontal", mode="determinate",
                maximum=1, value=0
            )
            bar.grid(row=0, column=2, sticky="ew", padx=5)
            frame.columnconfigure(2, weight=1)

            max_label = ttk.Label(frame, text="/ 0", width=9)
            max_label.grid(row=0, column=3, sticky="e")
            self.status_bars[key] = bar
            self.status_max_labels[key] = max_label

        ttk.Button(
            outer, text="RECUPERAR TUDO",
            command=self.recover_status
        ).grid(row=0, column=3, padx=8, pady=7)

    def status_changed(self, key):
        try:
            value = max(0, min(int(self.status_vars[key].get()), self.base_max[key]))
        except (ValueError, tk.TclError):
            value = 0
        self.status_vars[key].set(value)
        self.current_status[key] = value
        self.refresh_status_bar()

    def refresh_status_bar(self):
        for key in ("vida", "sanidade", "ocultismo"):
            maximum = max(0, int(self.base_max.get(key, 0)))
            try:
                current = max(0, min(int(self.status_vars[key].get()), maximum))
            except (ValueError, tk.TclError):
                current = 0
            self.status_vars[key].set(current)
            self.current_status[key] = current
            self.status_bars[key]["maximum"] = max(1, maximum)
            self.status_bars[key]["value"] = current
            self.status_max_labels[key].config(text=f"/ {maximum}")

    def recover_status(self):
        for key in self.status_vars:
            self.status_vars[key].set(self.base_max[key])
            self.current_status[key] = self.base_max[key]
        self.refresh_status_bar()
        self.add_history("STATUS", "Vida, Sanidade e Pontos de Ocultismo recuperados ao máximo.")

    # ------------------------------------------------------------
    # Tema visual
    # ------------------------------------------------------------
    def setup_theme(self):
        """Tema escuro inspirado em horror investigativo, sem dependências externas."""
        self.root.configure(bg="#09080d")
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#09080d")
        style.configure("TLabel", background="#09080d", foreground="#e9e4df", font=("Segoe UI", 10))
        style.configure("TNotebook", background="#09080d", borderwidth=0)
        style.configure("TNotebook.Tab", background="#17131d", foreground="#bcb5c4", padding=(14, 8), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#3a1725")], foreground=[("selected", "#ffffff")])
        style.configure("TButton", background="#3a1725", foreground="#ffffff", borderwidth=0, padding=(12, 7), font=("Segoe UI", 9, "bold"))
        style.map("TButton", background=[("active", "#5b2237"), ("pressed", "#24101a")])
        style.configure("Accent.TButton", background="#8f2f4e", foreground="#ffffff", padding=(14, 8), font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#b53e61"), ("pressed", "#6d213a")])
        style.configure("TEntry", fieldbackground="#141119", foreground="#f4eef0", insertcolor="#ffffff", bordercolor="#392b3c", padding=6)
        style.configure("TCombobox", fieldbackground="#141119", foreground="#f4eef0", background="#141119", arrowcolor="#d9a7b7", padding=5)
        style.map("TCombobox", fieldbackground=[("readonly", "#141119")], foreground=[("readonly", "#f4eef0")])
        style.configure("TSpinbox", fieldbackground="#141119", foreground="#f4eef0", background="#141119", arrowcolor="#d9a7b7", padding=5)
        style.configure("TLabelframe", background="#0f0d14", foreground="#e9e4df", bordercolor="#352839")
        style.configure("TLabelframe.Label", background="#0f0d14", foreground="#dca7b8", font=("Segoe UI", 10, "bold"))
        style.configure("TSeparator", background="#352839")
        style.configure("TProgressbar", troughcolor="#17131d", background="#9d3a59", bordercolor="#17131d", lightcolor="#9d3a59", darkcolor="#9d3a59")

    def build_header(self):
        header = tk.Frame(self.root, bg="#0f0b12", height=86, highlightthickness=1, highlightbackground="#3a1e2d")
        header.pack(fill="x", padx=8, pady=(8, 0))
        header.pack_propagate(False)

        canvas = tk.Canvas(header, width=70, height=70, bg="#0f0b12", highlightthickness=0)
        canvas.pack(side="left", padx=(14, 6), pady=8)
        canvas.create_oval(12, 12, 58, 58, outline="#9d3a59", width=2)
        canvas.create_line(35, 17, 35, 53, fill="#dca7b8", width=2)
        canvas.create_line(20, 45, 50, 45, fill="#dca7b8", width=2)
        canvas.create_polygon(35, 20, 47, 42, 23, 42, outline="#dca7b8", fill="", width=2)

        text = tk.Frame(header, bg="#0f0b12")
        text.pack(side="left", fill="both", expand=True, pady=10)
        tk.Label(text, text="DESCONJURAÇÃO", bg="#0f0b12", fg="#f4eef0", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(text, text="CRIADOR DE FICHA • INVESTIGAÇÃO PARANORMAL", bg="#0f0b12", fg="#b98fa0", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        canva_btn = tk.Button(
            header, text="CANVA", command=lambda: webbrowser.open(CANVA_PUBLIC_URL),
            bg="#17131d", fg="#dca7b8", activebackground="#3a1725",
            activeforeground="#ffffff", relief="flat", bd=0,
            font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10, pady=5
        )
        canva_btn.pack(side="right", padx=(4, 10))

        badge = tk.Label(header, text="D20", bg="#3a1725", fg="#ffffff", font=("Segoe UI", 14, "bold"), padx=18, pady=7)
        badge.pack(side="right", padx=4)

    # ------------------------------------------------------------
    # Construção das abas
    # ------------------------------------------------------------
    def build_ui(self):
        self.build_header()
        self.build_status_bar()

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_personal = ttk.Frame(nb)
        self.tab_attr = ttk.Frame(nb)
        self.tab_skill = ttk.Frame(nb)
        self.tab_progress = ttk.Frame(nb)
        self.tab_background = ttk.Frame(nb)
        self.tab_equipment = ttk.Frame(nb)
        self.tab_history = ttk.Frame(nb)
        self.tab_dice = ttk.Frame(nb)

        nb.add(self.tab_personal, text="1. Personagem")
        nb.add(self.tab_attr, text="2. Atributos")
        nb.add(self.tab_skill, text="3. Perícias")
        nb.add(self.tab_progress, text="4. Progressão")
        nb.add(self.tab_background, text="5. Antecedentes")
        nb.add(self.tab_equipment, text="6. Equipamentos")
        nb.add(self.tab_history, text="7. Histórico")
        nb.add(self.tab_dice, text="8. Rolagens")

        self.personal_ui()
        self.attr_ui()
        self.skill_ui()
        self.progress_ui()
        self.background_ui()
        self.equipment_ui()
        self.history_ui()
        self.dice_ui()

        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(
            bottom, text="↻ ATUALIZAR STATUS",
            command=self.update_status
        ).pack(side="left")
        ttk.Button(
            bottom, text="SALVAR JSON",
            command=self.save_json
        ).pack(side="left", padx=5)
        ttk.Button(
            bottom, text="CARREGAR JSON",
            command=self.load_json
        ).pack(side="left")
        ttk.Button(
            bottom, text="LIMPAR",
            command=self.clear
        ).pack(side="right")

    def personal_ui(self):
        fields = [
            ("Nome do personagem", "nome"),
            ("Nome do jogador", "jogador"),
            ("Idade", "idade"),
            ("Gênero", "genero"),
            ("Ocupação", "ocupacao"),
            ("Residência", "residencia"),
            ("Local de nascimento", "nascimento"),
        ]
        for i, (label, key) in enumerate(fields):
            ttk.Label(
                self.tab_personal, text=label + ":"
            ).grid(row=i, column=0, sticky="w", padx=10, pady=7)
            if key == "ocupacao":
                var = tk.StringVar()
                cb = ttk.Combobox(
                    self.tab_personal, textvariable=var,
                    values=sorted(OCCUPATIONS.keys()),
                    state="readonly", width=45
                )
                cb.grid(row=i, column=1, sticky="ew", padx=10, pady=7)
                cb.bind("<<ComboboxSelected>>", self.occupation_selected)
                self.vars[key] = var
            else:
                var = tk.StringVar()
                ttk.Entry(
                    self.tab_personal, textvariable=var, width=48
                ).grid(row=i, column=1, sticky="ew", padx=10, pady=7)
                self.vars[key] = var

        self.tab_personal.columnconfigure(1, weight=1)

        ttk.Label(
            self.tab_personal, text="NEX:"
        ).grid(row=8, column=0, sticky="w", padx=10, pady=7)

        nex_box = ttk.Combobox(
            self.tab_personal, textvariable=self.nex_var,
            values=self.NEX_VALUES, state="readonly", width=12
        )
        nex_box.grid(row=8, column=1, sticky="w", padx=10, pady=7)
        nex_box.bind("<<ComboboxSelected>>", lambda e: self.update_progression())

        ttk.Label(
            self.tab_personal,
            text="Escolha de 5% a 80% em intervalos de 5%. A progressão é recalculada automaticamente."
        ).grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        ttk.Label(
            self.tab_personal, text="Arquétipo / Nível de exposição:"
        ).grid(row=10, column=0, sticky="w", padx=10, pady=7)
        cb_arch = ttk.Combobox(
            self.tab_personal, textvariable=self.archetype_var,
            values=["Ainda não escolhido", "COMBATENTE", "INVESTIGADOR", "OCULTISTA"],
            state="readonly", width=30
        )
        cb_arch.grid(row=10, column=1, sticky="w", padx=10)
        cb_arch.bind("<<ComboboxSelected>>", lambda e: self.update_progression())

        ttk.Label(
            self.tab_personal,
            text="O arquétipo é desbloqueado em 30% conforme a árvore enviada."
        ).grid(row=11, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        ttk.Label(
            self.tab_personal,
            text="Grupo de 50%:"
        ).grid(row=12, column=0, sticky="w", padx=10, pady=7)
        group_cb = ttk.Combobox(
            self.tab_personal, textvariable=self.epic_group_var,
            values=[
                "Nenhum",
                "GUERREIRO DO SANGUE",
                "SOLDADO DA MORTE",
                "MENSAGEIRO DO CONHECIMENTO",
                "ANARQUISTA DA ENERGIA",
            ],
            state="readonly", width=35
        )
        group_cb.grid(row=12, column=1, sticky="w", padx=10)
        group_cb.bind("<<ComboboxSelected>>", lambda e: self.update_progression())

        ttk.Label(
            self.tab_personal,
            text="O grupo só aplica efeitos quando o NEX for 50% ou maior."
        ).grid(row=13, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        ttk.Label(
            self.tab_personal,
            text="Os ganhos de PV e PO abaixo são calculados a partir da árvore fornecida; Sanidade continua sendo POD × 5, pois as imagens não definem um ganho separado de Sanidade."
        ).grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=18)

    # ------------------------------------------------------------
    # Atributos
    # ------------------------------------------------------------
    def attr_ui(self):
        ttk.Label(
            self.tab_attr, text="Método de geração:"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.attr_mode = tk.StringVar(value="Médio")
        ttk.Combobox(
            self.tab_attr, textvariable=self.attr_mode,
            values=["Médio", "Pré-definidos", "Fácil", "Difícil"],
            state="readonly"
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(
            self.tab_attr,
            text="Campanha mediana: 4d6 por atributo, descartando o menor resultado.",
            foreground="#b9a9ad"
        ).grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 8))

        ttk.Button(
            self.tab_attr, text="🎲 ROLAR ATRIBUTOS • 4D6",
            command=self.generate_attrs,
            style="Accent.TButton"
        ).grid(row=0, column=2, padx=10)

        ttk.Label(
            self.tab_attr, text="Modo do teste:"
        ).grid(row=0, column=3, sticky="e", padx=(10, 4))
        ttk.Combobox(
            self.tab_attr, textvariable=self.roll_mode_var,
            values=["Normal", "Vantagem", "Desvantagem"],
            state="readonly", width=12
        ).grid(row=0, column=4, sticky="w")

        ttk.Label(
            self.tab_attr, text="Dado para testes:"
        ).grid(row=0, column=5, sticky="e", padx=(10, 4))
        ttk.Combobox(
            self.tab_attr, textvariable=self.dice_var,
            values=[f"d{i}" for i in DICE_VALUES],
            state="readonly", width=7
        ).grid(row=0, column=6, sticky="w")

        ttk.Label(
            self.tab_attr,
            text="Testes do sistema: d20 • Vantagem = menor resultado • Desvantagem = maior resultado"
        ).grid(row=0, column=7, sticky="w", padx=10)

        for i, (code, name) in enumerate(ATTRS, start=1):
            ttk.Label(
                self.tab_attr, text=f"{code} — {name}"
            ).grid(row=i, column=0, sticky="w", padx=10, pady=4)

            var = tk.IntVar(value=10)
            self.vars[code] = var
            ttk.Spinbox(
                self.tab_attr, from_=0, to=99,
                textvariable=var, width=8,
                command=self.update_status
            ).grid(row=i, column=1, sticky="w")

            ttk.Button(
                self.tab_attr, text="🎲 Rolar",
                command=lambda c=code: self.roll_attribute_test(c)
            ).grid(row=i, column=2, padx=5)

            result_label = tk.Label(
                self.tab_attr, text="—", width=24,
                font=("Arial", 10, "bold"), relief="groove"
            )
            result_label.grid(
                row=i, column=3, columnspan=3,
                sticky="w", padx=5
            )
            self.attr_roll_labels[code] = result_label

            effective = ttk.Label(self.tab_attr, text="Efetivo: 10")
            effective.grid(row=i, column=6, columnspan=2, sticky="w", padx=5)
            setattr(self, f"effective_attr_label_{code}", effective)

        ttk.Button(
            self.tab_attr, text="APLICAR BASES DAS PERÍCIAS",
            command=self.update_skill_bases
        ).grid(row=len(ATTRS) + 2, column=0, columnspan=3, pady=12)

        self.sanity_roll_button = ttk.Button(
            self.tab_attr,
            text="🧠 ROLAR SANIDADE • 1d100 < NEX",
            style="Accent.TButton",
            command=self.roll_sanity
        )
        self.sanity_roll_button.grid(
            row=len(ATTRS) + 2, column=3, columnspan=3, pady=12
        )

        ttk.Label(
            self.tab_attr,
            text="A rolagem de Sanidade usa 1d100 e é sucesso somente se o resultado for menor que o NEX atual."
        ).grid(
            row=len(ATTRS) + 3, column=0, columnspan=8,
            sticky="w", padx=10, pady=4
        )

    def generate_attrs(self):
        values = roll_attributes(self.attr_mode.get())
        for (code, _), value in zip(ATTRS, values):
            self.vars[code].set(value)
        self.update_progression()
        self.add_history("ATRIBUTOS", f"Atributos gerados pelo método: {self.attr_mode.get()}.")

    def selected_dice_sides(self):
        text = self.dice_var.get().lower().replace("d", "").strip()
        sides = int(text)
        if sides != 20:
            raise ValueError("Os testes de atributo e perícia usam exclusivamente d20 neste sistema.")
        return sides

    def roll_with_mode(self, sides):
        mode = self.roll_mode_var.get()
        if mode == "Normal":
            rolls = [random.randint(1, sides)]
        else:
            rolls = [random.randint(1, sides), random.randint(1, sides)]
        if mode == "Vantagem":
            result = min(rolls)
        elif mode == "Desvantagem":
            result = max(rolls)
        else:
            result = rolls[0]
        return rolls, result

    def roll_attribute_test(self, code):
        try:
            sides = self.selected_dice_sides()
            value = self.effective_attributes().get(code, self.vars[code].get())
            rolls, result = self.roll_with_mode(sides)
            outcome, tag = classify_roll(value, result)
            self.set_roll_result(
                self.attr_roll_labels[code], result, sides, outcome, tag,
                rolls=rolls, mode=self.roll_mode_var.get()
            )
            self.add_history(
                "ATRIBUTO",
                f"{code}: {rolls} → {result} ({outcome}) | {self.roll_mode_var.get()} | valor {value}"
            )
        except Exception as e:
            messagebox.showerror("Erro na rolagem", str(e))

    # ------------------------------------------------------------
    # Perícias
    # ------------------------------------------------------------
    def skill_ui(self):
        top = ttk.Frame(self.tab_skill)
        top.pack(fill="x", padx=10, pady=8)

        ttk.Label(top, text="Perícias ocupacionais sugeridas:").pack(side="left")
        self.occupation_label = ttk.Label(
            top, text="Escolha uma ocupação na aba Personagem."
        )
        self.occupation_label.pack(side="left", padx=8)

        ttk.Label(top, text="Dado:").pack(side="left", padx=(20, 4))
        ttk.Combobox(
            top, textvariable=self.dice_var,
            values=[f"d{i}" for i in DICE_VALUES],
            state="readonly", width=7
        ).pack(side="left")

        ttk.Label(top, text="Modo:").pack(side="left", padx=(15, 4))
        ttk.Combobox(
            top, textvariable=self.roll_mode_var,
            values=["Normal", "Vantagem", "Desvantagem"],
            state="readonly", width=12
        ).pack(side="left")

        canvas = tk.Canvas(self.tab_skill)
        scroll = ttk.Scrollbar(
            self.tab_skill, orient="vertical", command=canvas.yview
        )
        frame = ttk.Frame(canvas)

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(
            side="left", fill="both", expand=True,
            padx=(10, 0), pady=5
        )
        scroll.pack(side="right", fill="y", padx=(0, 10), pady=5)

        headers = ["Perícia", "Valor", "Teste", "Resultado", "Base"]
        for col, text in enumerate(headers):
            ttk.Label(
                frame, text=text, font=("Arial", 9, "bold")
            ).grid(
                row=0, column=col, sticky="w", padx=5, pady=(2, 5)
            )

        for r, name in enumerate(SKILLS, start=1):
            ttk.Label(
                frame, text=name, width=28
            ).grid(row=r, column=0, sticky="w", padx=5, pady=2)

            base = skill_base(name, {a: 10 for a, _ in ATTRS})
            var = tk.IntVar(value=base)
            self.skill_vars[name] = var

            ttk.Spinbox(
                frame, from_=0, to=100,
                textvariable=var, width=7
            ).grid(row=r, column=1, padx=5)

            ttk.Button(
                frame, text="🎲 Rolar",
                command=lambda n=name: self.roll_skill_test(n)
            ).grid(row=r, column=2, padx=5)

            result_label = tk.Label(
                frame, text="—", width=28,
                font=("Arial", 9, "bold"), relief="groove"
            )
            result_label.grid(row=r, column=3, sticky="w", padx=5)
            self.skill_roll_labels[name] = result_label

            ttk.Label(
                frame, text=f"Base: {SKILLS[name]}"
            ).grid(row=r, column=4, sticky="w")

        ttk.Button(
            frame, text="APLICAR BASES DOS ATRIBUTOS",
            command=self.update_skill_bases
        ).grid(
            row=len(SKILLS) + 2, column=0, columnspan=5, pady=12
        )

    def roll_skill_test(self, name):
        try:
            sides = self.selected_dice_sides()
            value = self.skill_vars[name].get()
            rolls, result = self.roll_with_mode(sides)
            outcome, tag = classify_roll(value, result)
            self.set_roll_result(
                self.skill_roll_labels[name], result, sides, outcome, tag,
                rolls=rolls, mode=self.roll_mode_var.get()
            )
            self.add_history(
                "PERÍCIA",
                f"{name}: {rolls} → {result} ({outcome}) | {self.roll_mode_var.get()} | valor {value}"
            )
        except Exception as e:
            messagebox.showerror("Erro na rolagem", str(e))

    def set_roll_result(self, label, result, sides, outcome, tag, rolls=None, mode="Normal"):
        backgrounds = {
            "normal": "#183b2a",
            "good": "#1d3557",
            "extreme": "#5b1d2c",
            "fail": "#211e26",
            "fail_extreme": "#4a1b28",
        }
        foregrounds = {
            "normal": "#a8e6bd",
            "good": "#a8c9ff",
            "extreme": "#ff9fb8",
            "fail": "#bcb5c4",
            "fail_extreme": "#ff9fb8",
        }
        extra = ""
        if rolls and len(rolls) > 1:
            extra = f" | rolagens: {rolls}"
        label.config(
            text=f"{result} ({outcome}){extra}",
            bg=backgrounds[tag],
            fg=foregrounds[tag]
        )

    def update_skill_bases(self):
        attrs = self.effective_attributes()
        for name, var in self.skill_vars.items():
            var.set(skill_base(name, attrs))

    def occupation_selected(self, event=None):
        occ = self.vars["ocupacao"].get()
        self.occupation_label.config(
            text=", ".join(OCCUPATIONS.get(occ, []))
        )
        self.update_skill_bases()

    # ------------------------------------------------------------
    # Progressão automatizada
    # ------------------------------------------------------------
    def attr_names(self):
        return [a for a, _ in ATTRS]

    def apply_capped_bonus(self, values, code, bonus, cap=None):
        if code not in values or code == "Nenhum":
            return
        if cap is None:
            values[code] += bonus
        else:
            values[code] = min(cap, values[code] + bonus)

    def effective_attributes(self):
        values = {code: int(self.vars[code].get()) for code, _ in ATTRS}

        # 25% — +1 atributo (Máx. 18)
        if self.nex_var.get() >= 25:
            self.apply_capped_bonus(values, self.progress_choices["attr25"].get(), 1, 18)

        # 30% — +1 atributo (Máx. 18)
        if self.nex_var.get() >= 30:
            self.apply_capped_bonus(values, self.progress_choices["attr30"].get(), 1, 18)

        arch = self.archetype_var.get()
        nex = self.nex_var.get()

        # Trocas de atributos do Ocultista.
        if nex >= 40 and arch == "OCULTISTA":
            a, b = self.progress_choices["swap40a"].get(), self.progress_choices["swap40b"].get()
            if a in values and b in values and a != b:
                values[a], values[b] = values[b], values[a]

        if nex >= 45 and arch == "OCULTISTA":
            a, b = self.progress_choices["swap45a"].get(), self.progress_choices["swap45b"].get()
            if a in values and b in values and a != b:
                values[a], values[b] = values[b], values[a]

        # 40%
        if nex >= 40:
            if arch in ("COMBATENTE", "INVESTIGADOR"):
                self.apply_capped_bonus(values, self.progress_choices["attr40"].get(), 1)
        # 45%
        if nex >= 45:
            if arch == "COMBATENTE":
                self.apply_capped_bonus(values, self.progress_choices["attr45a"].get(), 1)
            elif arch == "INVESTIGADOR":
                self.apply_capped_bonus(values, self.progress_choices["attr45a"].get(), 2)

        # 50% — grupos finais.
        if nex >= 50:
            group = self.epic_group_var.get()
            if group == "GUERREIRO DO SANGUE":
                self.apply_capped_bonus(values, self.progress_choices["group_attr1"].get(), 2)
            elif group == "SOLDADO DA MORTE":
                for key in ("group_attr1", "group_attr2", "group_attr3"):
                    self.apply_capped_bonus(values, self.progress_choices[key].get(), 2)
            elif group == "MENSAGEIRO DO CONHECIMENTO":
                self.apply_capped_bonus(values, self.progress_choices["group_attr1"].get(), 2)
            elif group == "ANARQUISTA DA ENERGIA":
                for code in values:
                    values[code] += 1

        return values

    def progression_numeric_bonus(self):
        """
        Retorna os bônus cumulativos explicitamente indicados nas três imagens.
        Frações são convertidas para pontos inteiros com int(), preservando o
        mesmo comportamento inteiro da ficha atual.
        """
        nex = self.nex_var.get()
        arch = self.archetype_var.get()
        group = self.epic_group_var.get()

        con = int(self.vars["CON"].get())
        pod = int(self.vars["POD"].get())

        life = 0
        occult = 0

        if nex >= 5:
            life += int(con / 2)

        for level in (10, 15, 20):
            if nex >= level:
                occult += int(pod / 5)

        if nex >= 25:
            life += int(con / 2)
            occult += int(pod / 5)

        if nex >= 30:
            if arch == "COMBATENTE":
                life += int(con / 2)
            elif arch == "OCULTISTA":
                occult += int(pod / 4)

        if nex >= 35:
            if arch in ("COMBATENTE", "INVESTIGADOR"):
                life += int(con / 2)
            elif arch == "OCULTISTA":
                life += int(con / 4)
            occult += int(pod / 5)

        if nex >= 40:
            if arch == "COMBATENTE":
                life += int(con / 2)
                occult += int(pod / 5)
            elif arch == "INVESTIGADOR":
                life += int(con / 4)
                occult += int(pod / 5)
            elif arch == "OCULTISTA":
                life += int(con / 4)
                occult += int(pod / 4)

        if nex >= 45:
            if arch in ("COMBATENTE",):
                life += int(con / 2)
                occult += int(pod / 5)
            elif arch == "INVESTIGADOR":
                life += int(con / 4)
                occult += int(pod / 5)
            elif arch == "OCULTISTA":
                life += int(con / 4)
                occult += int(pod / 4)

        if nex >= 50:
            if group in (
                "GUERREIRO DO SANGUE",
                "SOLDADO DA MORTE",
                "MENSAGEIRO DO CONHECIMENTO",
                "ANARQUISTA DA ENERGIA",
            ):
                life += int(con / 2)
                occult += int(pod / 2)

        return life, occult

    def progression_effects(self):
        nex = self.nex_var.get()
        arch = self.archetype_var.get()
        group = self.epic_group_var.get()
        effects = []

        # Conteúdo transcrito das imagens, aplicado cumulativamente.
        entries = {
            5: ["+½ CON em Pontos de Vida"],
            10: ["+⅕ POD em Pontos de Ocultismo"],
            15: ["+⅕ POD em Pontos de Ocultismo"],
            20: ["+⅕ POD em Pontos de Ocultismo"],
            25: ["+½ CON em Pontos de Vida", "+1 Atributo (Máx. 18)", "+⅕ POD em Pontos de Ocultismo"],
            30: ["+1 Atributo (Máx. 18)", "Escolha um Arquétipo"],
            35: ["+1 Habilidade ou Ritual", "+⅕ POD em Pontos de Ocultismo"],
            40: ["+1 Atributo sem máximo", "+⅕ POD em Pontos de Ocultismo"],
            45: ["Recupera todos os Pontos de Vida e Ocultismo", "+1 Ritual"],
            50: ["Escolha um dos quatro grupos finais"],
        }

        for level in self.NEX_VALUES:
            if level > nex:
                break
            for text in entries.get(level, []):
                effects.append(f"{level}% — {text}")

        if nex >= 30 and arch != "Ainda não escolhido":
            if arch == "COMBATENTE":
                effects.append("30% — COMBATENTE: +½ CON em PV; +1 Habilidade")
            elif arch == "INVESTIGADOR":
                effects.append("30% — INVESTIGADOR: +1 em 8 perícias; +1 Habilidade")
            elif arch == "OCULTISTA":
                effects.append("30% — OCULTISTA: +¼ POD em PO; +1 Habilidade ou Ritual")

        if nex >= 35 and arch:
            if arch == "COMBATENTE":
                effects.append("35% — COMBATENTE: +½ CON em PV; +1 Habilidade/Ritual")
            elif arch == "INVESTIGADOR":
                effects.append("35% — INVESTIGADOR: +½ CON em PV; +1 Habilidade/Ritual")
            elif arch == "OCULTISTA":
                effects.append("35% — OCULTISTA: +¼ CON em PV; +1 Habilidade/Ritual")

        if nex >= 40 and arch:
            if arch == "COMBATENTE":
                effects.append("40% — COMBATENTE: +½ CON em PV; +1 Atributo")
            elif arch == "INVESTIGADOR":
                effects.append("40% — INVESTIGADOR: +¼ CON em PV; +1 Atributo")
            elif arch == "OCULTISTA":
                effects.append("40% — OCULTISTA: +¼ CON em PV; trocar 2 atributos (Máx. 20)")

        if nex >= 45 and arch:
            if arch == "COMBATENTE":
                effects.append("45% — COMBATENTE: +½ CON em PV; +1 Atributo; +1 Ritual")
            elif arch == "INVESTIGADOR":
                effects.append("45% — INVESTIGADOR: +¼ CON em PV; +2 Atributos; +1 Ritual")
            elif arch == "OCULTISTA":
                effects.append("45% — OCULTISTA: +¼ CON em PV; trocar 2 atributos; +2 Rituais; usar PV como PO; 2º Círculo")

        if nex >= 50 and group != "Nenhum":
            group_text = {
                "GUERREIRO DO SANGUE": "50% — GUERREIRO DO SANGUE: +½ CON em PV; +2 Atributo; +1 Habilidade/Ritual; vantagem em Rituais de Sangue; +½ POD em PO; sem ingredientes de Sangue.",
                "SOLDADO DA MORTE": "50% — SOLDADO DA MORTE: +½ CON em PV; +2 em 3 Atributos; +1 Habilidade/Ritual; vantagem em Rituais de Morte; +½ POD em PO; sem ingredientes de Morte.",
                "MENSAGEIRO DO CONHECIMENTO": "50% — MENSAGEIRO DO CONHECIMENTO: +½ CON em PV; +2 Atributo; +1 Habilidade/Ritual; vantagem em Rituais de Conhecimento; +½ POD em PO; sem ingredientes de Conhecimento.",
                "ANARQUISTA DA ENERGIA": "50% — ANARQUISTA DA ENERGIA: +½ CON em PV; +1 em todos os Atributos; +1 Habilidade/Ritual; vantagem em Rituais de Energia; +½ POD em PO; sem ingredientes de Energia.",
            }
            effects.append(group_text[group])

        if nex >= 55:
            effects.append("55% — Sem efeitos adicionais definidos nas três imagens enviadas.")
        if nex >= 60:
            effects.append("60% — Sem efeitos adicionais definidos nas três imagens enviadas.")
        if nex >= 65:
            effects.append("65% — Sem efeitos adicionais definidos nas três imagens enviadas.")
        if nex >= 70:
            effects.append("70% — Sem efeitos adicionais definidos nas três imagens enviadas.")
        if nex >= 75:
            effects.append("75% — Sem efeitos adicionais definidos nas três imagens enviadas.")
        if nex >= 80:
            effects.append("80% — Sem efeitos adicionais definidos nas três imagens enviadas.")

        return effects

    def progress_ui(self):
        left = ttk.Frame(self.tab_progress)
        left.pack(side="left", fill="y", padx=10, pady=10)

        right = ttk.Frame(self.tab_progress)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(
            left, text="ESCOLHAS DA PROGRESSÃO",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        attr_values = ["Nenhum"] + self.attr_names()

        self.choice_widgets = []

        def add_choice(parent, label, key, values=attr_values):
            row = ttk.Frame(parent)
            row.pack(fill="x", pady=3)
            ttk.Label(row, text=label, width=30).pack(side="left")
            cb = ttk.Combobox(
                row, textvariable=self.progress_choices[key],
                values=values, state="readonly", width=22
            )
            cb.pack(side="left")
            cb.bind("<<ComboboxSelected>>", lambda e: self.update_progression())
            self.choice_widgets.append((key, cb))
            return cb

        add_choice(left, "25% — atributo +1 (máx. 18)", "attr25")
        add_choice(left, "30% — atributo +1 (máx. 18)", "attr30")
        add_choice(left, "40% — atributo +1", "attr40")
        add_choice(left, "45% — atributo +1/+2", "attr45a")
        add_choice(left, "45% — 2º atributo (Investigador)", "attr45b")

        ttk.Separator(left).pack(fill="x", pady=8)
        ttk.Label(left, text="Trocas do Ocultista").pack(anchor="w", pady=3)
        add_choice(left, "40% — atributo A", "swap40a")
        add_choice(left, "40% — atributo B", "swap40b")
        add_choice(left, "45% — atributo A", "swap45a")
        add_choice(left, "45% — atributo B", "swap45b")

        ttk.Separator(left).pack(fill="x", pady=8)
        ttk.Label(left, text="Grupo de 50%").pack(anchor="w", pady=3)
        add_choice(left, "Grupo — atributo 1", "group_attr1")
        add_choice(left, "Grupo — atributo 2", "group_attr2")
        add_choice(left, "Grupo — atributo 3", "group_attr3")

        ttk.Label(
            left,
            text="Os campos de escolha só alteram os atributos quando o respectivo NEX/arquétipo estiver desbloqueado."
        ).pack(anchor="w", pady=10)

        ttk.Label(
            right, text="PROGRESSÃO DESBLOQUEADA",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.progress_status = ttk.Label(right, text="")
        self.progress_status.pack(anchor="w", pady=(3, 10))

        self.progress_text = tk.Text(
            right, width=70, height=28, wrap="word"
        )
        self.progress_text.pack(fill="both", expand=True)
        self.progress_text.config(state="disabled")

    def update_progression(self):
        try:
            nex = int(self.nex_var.get())
        except (ValueError, tk.TclError):
            nex = 5
            self.nex_var.set(5)

        if nex < 30:
            self.archetype_var.set("Ainda não escolhido")
        if nex < 50:
            self.epic_group_var.set("Nenhum")

        base_attrs = self.effective_attributes()
        for code, _ in ATTRS:
            label = getattr(self, f"effective_attr_label_{code}", None)
            if label:
                label.config(text=f"Efetivo: {base_attrs[code]}")

        for key, widget in getattr(self, "choice_widgets", []):
            # Desabilitação é cosmética; os valores permanecem salvos.
            widget.configure(state="readonly")

        effects = self.progression_effects()
        self.progress_text.config(state="normal")
        self.progress_text.delete("1.0", "end")
        self.progress_text.insert(
            "end",
            f"NEX ATUAL: {nex}%\n"
            f"ARQUÉTIPO: {self.archetype_var.get()}\n"
            f"GRUPO DE 50%: {self.epic_group_var.get()}\n\n"
        )
        if effects:
            self.progress_text.insert("end", "\n".join(f"• {e}" for e in effects))
        else:
            self.progress_text.insert("end", "Nenhuma progressão selecionada.")
        self.progress_text.config(state="disabled")

        self.update_status()

    # ------------------------------------------------------------
    # Status e Sanidade
    # ------------------------------------------------------------
    def update_status(self):
        try:
            a = self.effective_attributes()
            base_life = (a["CON"] + a["TAM"]) // 2
            base_sanity = a["POD"] * 5
            base_occult = a["POD"]

            bonus_life, bonus_occult = self.progression_numeric_bonus()

            life = base_life + bonus_life
            sanity = base_sanity
            occult = base_occult + bonus_occult

            old_max = dict(self.base_max)
            self.base_max = {
                "vida": max(0, life),
                "sanidade": max(0, sanity),
                "ocultismo": max(0, occult),
            }

            # Primeiro cálculo: se nunca houve status, começa cheio.
            for key in self.status_vars:
                if old_max.get(key, 0) == 0:
                    self.status_vars[key].set(self.base_max[key])
                else:
                    try:
                        current = int(self.status_vars[key].get())
                    except (ValueError, tk.TclError):
                        current = self.base_max[key]
                    self.status_vars[key].set(
                        min(current, self.base_max[key])
                    )

            # 45% recupera PV e PO.
            if self.nex_var.get() >= 45 and self.nex_var.get() != getattr(self, "_last_nex_for_recovery", None):
                if self.nex_var.get() == 45 or getattr(self, "_last_nex_for_recovery", 0) < 45:
                    self.status_vars["vida"].set(self.base_max["vida"])
                    self.status_vars["ocultismo"].set(self.base_max["ocultismo"])
                    self.add_history(
                        "PROGRESSÃO",
                        "45% alcançado: PV e Pontos de Ocultismo recuperados ao máximo."
                    )
            self._last_nex_for_recovery = self.nex_var.get()

            self.refresh_status_bar()
            self.update_skill_bases()

            for code, _ in ATTRS:
                label = getattr(self, f"effective_attr_label_{code}", None)
                if label:
                    label.config(text=f"Efetivo: {a[code]}")

            if hasattr(self, "status"):
                self.status.delete("1.0", "end")
                self.status.insert(
                    "end",
                    f"VIDA: {life}\n"
                    f"SANIDADE: {sanity}\n"
                    f"PONTOS DE OCULTISMO: {occult}\n"
                    f"MOVIMENTO: {calc_mov(a['FOR'], a['DES'], a['TAM'])}\n"
                    f"DANO EXTRA: {damage_bonus_and_body(a['FOR'], a['TAM'])[0]}\n"
                    f"CORPO: {damage_bonus_and_body(a['FOR'], a['TAM'])[1]}\n"
                    f"NEX: {self.nex_var.get()}%\n\n"
                    f"TESTES: d20.\n"
                    f"Modo: Normal / Vantagem / Desvantagem.\n"
                )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def roll_sanity(self):
        nex = int(self.nex_var.get())
        result = random.randint(1, 100)
        success = result < nex
        outcome = "SUCESSO" if success else "FALHA"
        if hasattr(self, "sanity_roll_button"):
            self.sanity_roll_button.config(
                text=f"🧠 {result}/100 — {outcome}"
            )
        self.add_history(
            "SANIDADE",
            f"1d100 = {result} | NEX {nex}% | precisa ser < {nex} | {outcome}"
        )
        messagebox.showinfo(
            "Teste de Sanidade",
            f"1d100: {result}\nNEX: {nex}%\n\n{outcome}\n\n"
            f"Regra: o resultado deve ser menor que o NEX."
        )

    # ------------------------------------------------------------
    # Antecedentes / Equipamentos
    # ------------------------------------------------------------
    def background_ui(self):
        labels = [
            ("Descrição pessoal", "descricao"),
            ("Ideologia / crenças", "ideologia"),
            ("Pessoas significativas", "pessoas"),
            ("Locais importantes", "locais"),
            ("Pertences queridos", "pertences"),
            ("Características", "caracteristicas"),
            ("Ferimentos e cicatrizes", "ferimentos"),
            ("Traumas", "traumas"),
            ("Livros ocultistas, rituais e artefatos", "ocultistas"),
            ("Encontros com entidades estranhas", "entidades"),
            ("Conexão chave", "conexao"),
        ]
        for i, (label, key) in enumerate(labels):
            ttk.Label(
                self.tab_background, text=label + ":"
            ).grid(
                row=i, column=0, sticky="nw", padx=10, pady=6
            )
            text = tk.Text(
                self.tab_background, width=75,
                height=3 if i < 6 else 4
            )
            text.grid(
                row=i, column=1, sticky="ew", padx=10, pady=6
            )
            self.vars[key] = text
        self.tab_background.columnconfigure(1, weight=1)

        ttk.Button(
            self.tab_background,
            text="GERAR INSPIRAÇÃO ALEATÓRIA",
            command=self.random_background
        ).grid(row=11, column=0, columnspan=2, pady=10)

    def random_background(self):
        ideas = {
            "descricao": [
                "Magro e pálido", "Robusto e musculoso",
                "Desleixado e cansado", "Elegante e reservado",
                "Carrancudo e forte"
            ],
            "ideologia": [
                "Existe um poder superior que venero.",
                "A humanidade pode viver bem sem religião.",
                "A ciência tem todas as respostas.",
                "Acredito no destino.",
                "Acredito no oculto."
            ],
            "pessoas": [
                "Pais", "Irmão", "Amigo de infância",
                "Pessoa que ensinou minha maior perícia",
                "Colega investigador", "NPC do jogo"
            ],
            "locais": [
                "Cidade natal", "Universidade", "Biblioteca",
                "Casa da família", "Local de trabalho",
                "Lugar onde fui mais feliz"
            ],
            "pertences": [
                "Item ligado à maior perícia",
                "Objeto essencial para a ocupação",
                "Lembrança da infância", "Fotografia ou carta",
                "Animal de estimação"
            ],
            "caracteristicas": [
                "Generoso", "Bom com animais", "Sonhador",
                "Apostador", "Bom cozinheiro", "Leal", "Ambicioso"
            ],
        }
        for key, options in ideas.items():
            self.vars[key].delete("1.0", "end")
            self.vars[key].insert("1.0", random.choice(options))

    def equipment_ui(self):
        ttk.Label(
            self.tab_equipment,
            text="Dinheiro inicial: 3d6 × R$100"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.money_var = tk.StringVar(value="—")
        ttk.Label(
            self.tab_equipment, textvariable=self.money_var,
            font=("Arial", 14, "bold")
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(
            self.tab_attr,
            text="Campanha mediana: 4d6 por atributo, descartando o menor resultado.",
            foreground="#b9a9ad"
        ).grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 8))

        ttk.Button(
            self.tab_equipment,
            text="ROLAR DINHEIRO",
            command=self.roll_money
        ).grid(row=0, column=2, padx=10)

        ttk.Label(
            self.tab_equipment,
            text="Inventário (item / quantidade / peso):"
        ).grid(row=2, column=0, columnspan=3, sticky="w", padx=10)
        self.inventory = tk.Text(
            self.tab_equipment, width=90, height=20
        )
        self.inventory.grid(
            row=3, column=0, columnspan=3,
            padx=10, pady=8, sticky="nsew"
        )

        self.capacity = tk.StringVar(
            value="Capacidade padrão: 16 kg / 16 slots"
        )
        ttk.Label(
            self.tab_equipment,
            textvariable=self.capacity
        ).grid(
            row=4, column=0, columnspan=3,
            sticky="w", padx=10
        )
        self.tab_equipment.columnconfigure(1, weight=1)
        self.tab_equipment.rowconfigure(3, weight=1)

    def roll_money(self):
        total = roll(3, 6) * 100
        value = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.money_var.set(value)
        self.add_history("DADOS", f"Dinheiro: 3d6 × R$100 = {value}")

    # ------------------------------------------------------------
    # Histórico
    # ------------------------------------------------------------
    def history_ui(self):
        top = ttk.Frame(self.tab_history)
        top.pack(fill="x", padx=10, pady=8)

        ttk.Button(
            top, text="LIMPAR HISTÓRICO",
            command=self.clear_history
        ).pack(side="left")

        ttk.Button(
            top, text="ATUALIZAR",
            command=self.refresh_history
        ).pack(side="left", padx=5)

        self.history_text = tk.Text(
            self.tab_history, wrap="word", state="disabled"
        )
        self.history_text.pack(
            fill="both", expand=True, padx=10, pady=(0, 10)
        )

    def add_history(self, category, message):
        from datetime import datetime
        stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.history.append({
            "timestamp": stamp,
            "category": category,
            "message": message,
        })
        self.refresh_history()

    def refresh_history(self):
        if not hasattr(self, "history_text"):
            return
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        if not self.history:
            self.history_text.insert("end", "Nenhuma rolagem registrada.")
        else:
            for item in self.history:
                self.history_text.insert(
                    "end",
                    f"[{item['timestamp']}] [{item['category']}] {item['message']}\n"
                )
        self.history_text.config(state="disabled")

    def clear_history(self):
        self.history.clear()
        self.refresh_history()

    # ------------------------------------------------------------
    # Rolagens quaisquer
    # ------------------------------------------------------------
    def dice_ui(self):
        top = ttk.Frame(self.tab_dice)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(top, text="Expressão:").pack(side="left")
        self.custom_dice_var = tk.StringVar(value="1d20")
        ttk.Entry(
            top, textvariable=self.custom_dice_var, width=15
        ).pack(side="left", padx=7)

        ttk.Button(
            top, text="🎲 ROLAR",
            command=self.roll_custom_dice
        ).pack(side="left")

        ttk.Label(
            top,
            text="Exemplos: d20, 2d6, 3d8+2, 4d10-1"
        ).pack(side="left", padx=12)

        self.dice_result = tk.Label(
            self.tab_dice,
            text="—",
            font=("Arial", 22, "bold"),
            relief="groove",
            width=35,
            height=3
        )
        self.dice_result.pack(padx=10, pady=10)

        self.dice_log = tk.Text(
            self.tab_dice, height=20, state="disabled"
        )
        self.dice_log.pack(
            fill="both", expand=True, padx=10, pady=10
        )

    def roll_custom_dice(self):
        import re
        expr = self.custom_dice_var.get().strip().lower().replace(" ", "")
        match = re.fullmatch(r"(?:(\d+)?d(\d+)|(\d+))(?:([+-])(\d+))?", expr)
        if not match:
            messagebox.showerror(
                "Rolagem inválida",
                "Use formatos como d20, 2d6, 3d8+2 ou 4d10-1."
            )
            return

        dice_count = int(match.group(1) or (1 if match.group(3) is None else 0))
        sides = int(match.group(2) or 0)
        modifier = int(match.group(5) or 0)
        if match.group(4) == "-":
            modifier = -modifier

        if match.group(3) is not None:
            # Número puro, ex.: 20
            rolls = [int(match.group(3))]
            total = rolls[0] + modifier
        else:
            if dice_count < 1 or dice_count > 100:
                raise ValueError("Use de 1 a 100 dados.")
            if sides < 2 or sides > 1000:
                raise ValueError("Os dados devem ter de 2 a 1000 lados.")
            rolls = [random.randint(1, sides) for _ in range(dice_count)]
            total = sum(rolls) + modifier

        mod_text = f"{modifier:+d}" if modifier else ""
        self.dice_result.config(
            text=f"{expr} = {total}\nRolagens: {rolls}{mod_text}"
        )
        self.dice_log.config(state="normal")
        self.dice_log.insert(
            "end", f"{expr} → {rolls} {mod_text} = {total}\n"
        )
        self.dice_log.config(state="disabled")
        self.add_history(
            "DADOS",
            f"{expr} → {rolls} {mod_text} = {total}"
        )

    # ------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------
    def collect(self):
        data = {
            "personagem": {},
            "atributos": {},
            "pericias": {},
            "antecedentes": {},
            "equipamentos": {},
            "progressao": {},
            "status": dict(self.current_status),
            "historico": list(self.history),
        }

        for key in [
            "nome", "jogador", "idade", "genero",
            "ocupacao", "residencia", "nascimento"
        ]:
            data["personagem"][key] = self.vars[key].get()

        data["personagem"]["nex"] = int(self.nex_var.get())
        data["personagem"]["arquetipo"] = self.archetype_var.get()
        data["personagem"]["grupo_50"] = self.epic_group_var.get()

        for code, _ in ATTRS:
            data["atributos"][code] = self.vars[code].get()

        for name, var in self.skill_vars.items():
            data["pericias"][name] = var.get()

        for key in [
            "descricao", "ideologia", "pessoas", "locais",
            "pertences", "caracteristicas", "ferimentos",
            "traumas", "ocultistas", "entidades", "conexao"
        ]:
            data["antecedentes"][key] = self.vars[key].get("1.0", "end").strip()

        data["equipamentos"]["dinheiro"] = self.money_var.get()
        data["equipamentos"]["inventario"] = self.inventory.get("1.0", "end").strip()

        data["progressao"]["escolhas"] = {
            key: var.get()
            for key, var in self.progress_choices.items()
        }

        data["status"] = {
            key: int(var.get())
            for key, var in self.status_vars.items()
        }
        data["historico"] = list(self.history)
        return data

    def save_json(self):
        data = self.collect()
        path = filedialog.asksaveasfilename(
            title="Salvar ficha",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Sucesso", "Ficha salva.")

    def load_json(self):
        path = filedialog.askopenfilename(
            title="Carregar ficha",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in data.get("personagem", {}).items():
            if key in self.vars and isinstance(self.vars[key], tk.StringVar):
                self.vars[key].set(value)

        self.nex_var.set(
            int(data.get("personagem", {}).get("nex", 5))
        )
        self.archetype_var.set(
            data.get("personagem", {}).get("arquetipo", "Ainda não escolhido")
        )
        self.epic_group_var.set(
            data.get("personagem", {}).get("grupo_50", "Nenhum")
        )

        for key, value in data.get("atributos", {}).items():
            if key in self.vars:
                self.vars[key].set(value)

        for key, value in data.get("pericias", {}).items():
            if key in self.skill_vars:
                self.skill_vars[key].set(value)

        for key, value in data.get("antecedentes", {}).items():
            if key in self.vars and isinstance(self.vars[key], tk.Text):
                self.vars[key].delete("1.0", "end")
                self.vars[key].insert("1.0", value)

        self.money_var.set(
            data.get("equipamentos", {}).get("dinheiro", "—")
        )
        self.inventory.delete("1.0", "end")
        self.inventory.insert(
            "1.0", data.get("equipamentos", {}).get("inventario", "")
        )

        for key, value in data.get("progressao", {}).get("escolhas", {}).items():
            if key in self.progress_choices:
                self.progress_choices[key].set(value)

        self.history = data.get("historico", [])
        saved_status = data.get("status", {})
        self.update_progression()

        for key, value in saved_status.items():
            if key in self.status_vars:
                try:
                    self.status_vars[key].set(
                        min(max(0, int(value)), self.base_max[key])
                    )
                except (ValueError, TypeError):
                    pass
        self.refresh_status_bar()
        self.refresh_history()
        messagebox.showinfo("Sucesso", "Ficha carregada.")

    def clear(self):
        if not messagebox.askyesno("Confirmar", "Limpar toda a ficha?"):
            return

        for key, var in self.vars.items():
            if isinstance(var, tk.StringVar):
                var.set("")
            elif isinstance(var, tk.IntVar):
                var.set(10)
            elif isinstance(var, tk.Text):
                var.delete("1.0", "end")

        self.nex_var.set(5)
        self.archetype_var.set("Ainda não escolhido")
        self.epic_group_var.set("Nenhum")

        for var in self.progress_choices.values():
            var.set("Nenhum")

        self.money_var.set("—")
        self.inventory.delete("1.0", "end")
        self.history.clear()

        for key in self.status_vars:
            self.status_vars[key].set(0)

        self.update_progression()
        self.refresh_history()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
