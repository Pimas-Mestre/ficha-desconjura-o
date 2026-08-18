# Desconjuração — Criador de Ficha

Aplicativo desktop em Python/Tkinter para criação e gerenciamento de fichas do sistema **Desconjuração**, baseado no PDF fornecido.

## O que foi ajustado

- Interface redesenhada com tema escuro, visual de horror investigativo e melhor hierarquia visual.
- Testes de **atributos e perícias padronizados em d20**, conforme a seção de regras do sistema.
- Geração padrão de atributos em **4d6, descartando o menor dado**, conforme a campanha mediana descrita no PDF. Também estão disponíveis os métodos Pré-definidos, Fácil e Difícil.
- Rolagem de Sanidade permanece em 1d100 com a regra de comparação ao NEX.
- Salvamento e carregamento de ficha em JSON.
- Histórico de rolagens.
- Progressão de NEX, arquétipos e grupos de 50% conforme os dados já presentes no código.
- Rolador livre continua aceitando expressões como `d20`, `2d6`, `3d8+2` e `4d10-1`.
- Integração opcional com um endereço público do Canva por meio da variável `DESCONJURACAO_CANVA_URL`.

## Base do sistema

O PDF determina que os testes usam a **Tabela do Valor de Habilidade** ao rolar um d20, aplicável tanto a atributos quanto a perícias. A criação dos atributos permanece separada dessa rolagem de testes: por padrão, cada atributo é gerado com **4d6, descartando o menor resultado**. A tabela define os graus Normal, Bom e Extremo de acordo com o valor da habilidade.

O programa também preserva as regras de Vida, Sanidade, Pontos de Ocultismo, Movimento, Corpo e Dano Extra já implementadas na versão enviada.

## Como executar

### Windows

Instale Python 3.10+ e execute:

```bash
python desconjuracao.py
```

### Linux

Em distribuições Debian/Ubuntu, caso o Tkinter não esteja instalado:

```bash
sudo apt install python3-tk
python3 desconjuracao.py
```

### macOS

Com Python 3.10+ instalado:

```bash
python3 desconjuracao.py
```

O projeto não exige pacotes externos de Python.

## Canva

O Canva não é uma dependência obrigatória. Para usar um design/banner público como referência ou atalho dentro do programa, defina uma URL pública:

**Windows PowerShell**

```powershell
$env:DESCONJURACAO_CANVA_URL="COLE_AQUI_A_URL_PUBLICA_DO_CANVA"
python desconjuracao.py
```

**Linux/macOS**

```bash
export DESCONJURACAO_CANVA_URL="COLE_AQUI_A_URL_PUBLICA_DO_CANVA"
python3 desconjuracao.py
```

Também é possível exportar do Canva um banner em PNG e colocá-lo em `assets/canva/`. O código não depende desse arquivo para iniciar.

## Estrutura

```text
.
├── desconjuracao.py
├── README.md
├── requirements.txt
├── .gitignore
├── assets/
│   └── canva/
│       └── README.md
└── tests/
    └── test_regras.py
```

## GitHub

```bash
git init
git add .
git commit -m "feat: criador de ficha Desconjuração com d20"
git branch -M main
git remote add origin SEU_REPOSITORIO
 git push -u origin main
```

> Observação: este projeto é uma aplicação desktop Tkinter. Ele pode ser armazenado e versionado normalmente no GitHub, mas não roda diretamente como página do GitHub Pages.
