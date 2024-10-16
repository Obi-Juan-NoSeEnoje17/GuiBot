def format_date_date(date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    return day + " " + month + " " + year

def format_date_title(date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    return year + "-" + month + "-" + day

def check_date(date):
    return len(date.split("-")) != 3

def points_of_day(type):
    latex_content = ""
    with open ('points_of_day_' + type + '.txt', 'r') as points_of_day_read:
        for point_of_day in points_of_day_read:
            title = point_of_day.strip().split(":")[0]
            desc = point_of_day.strip().split(": ")[1]
            latex_content = latex_content + "        \\subsection{" + title + "}\n            " + desc + "\n"
    return latex_content

def create_latex_content(type, date):
    latex_content = fr"""
    \documentclass{{article}}
    \usepackage[utf8]{{inputenc}}
    \usepackage[utf8]{{inputenc}}
    \usepackage[left=2.5cm, top=3.5cm, right=2.5cm, bottom=3.5cm]{{geometry}}
    \usepackage[usenames, dvipsnames, svgnames, table, xcdraw]{{xcolor}}
    \usepackage[spanish,es-tabla]{{babel}}
    \usepackage{{float}}
    \usepackage{{amsmath, amsthm, amssymb, tabu}}
    \usepackage[breaklinks=true]{{hyperref}} % Referencias
    \usepackage{{longtable}} \usepackage{{multirow}} \usepackage{{multicol}}
    \usepackage{{graphicx}} \usepackage{{fancyhdr}}
    \usepackage{{makeidx}} \usepackage{{enumitem}}
    \usepackage{{varwidth}} \usepackage{{tasks}}
    \usepackage{{amsfonts}} \usepackage{{ragged2e}}
    \usepackage{{amssymb}} % Símbolos en notación matemáticos con el \mathbb
    \usepackage{{wrapfig}} % Alinear imágenes con respecto al text
    \usepackage{{caption}} \usepackage{{subcaption}}
    \usepackage{{upquote}}
    \usepackage{{color}} \usepackage{{fancyvrb}} 
    \usepackage{{listings}}
    \usepackage[numbered,framed]{{matlab-prettifier}}
    \usepackage{{subfiles}}

    \hypersetup{{colorlinks=true,                     %habilitar colorear enlaces
    linkcolor=blue,
    filecolor=magenta,                
    urlcolor=cyan,
    }}

    \begin{{document}}
    \newpage

    \title{{{type}}}
    \date{{{date}}}
    \maketitle
    \begin{{center}}
        \includegraphics[scale=0.25]{{Logo GUI.jpg}}
    \end{{center}}
    \newpage
    \tableofcontents
    \newpage
    \section{{Asistentes}}
        \subsection{{Lista de asistentes}}
            \begin{{table}}[h!]
                \centering
                \begin{{tabular}}{{c|c}}
                    Asistentes & Justifican su ausencia \\
                    & 
                \end{{tabular}}
                \label{{tab:asistentes}}
            \end{{table}}
    \section{{rden del día}}
        \subsection{{Aprobación del acta de la sesión anterior}}
{points_of_day(type)}
        
        
        
        
        
        
        
        \vfill
    \begin{{center}}Sin más asuntos que tratar queda finalizada la presente Junta \end{{center}}
    \begin{{center}} Valladolid {date} \end{{center}}
    \begin{{center}} Constan a continuación la firma del secretario y el presidente con el sello de la asociación\end{{center}}

    \begin{{table}}[htpp]
    \centering
    \begin{{tabular}}{{lllll}}
    El secretario &  & & & El presidente \\
                &  & & &        
    \end{{tabular}}
    \end{{table}}\vspace{{1.5cm}}

    \end{{document}}
    """
    return latex_content