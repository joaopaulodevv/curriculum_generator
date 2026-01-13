#!/usr/bin/env python3
"""
Script simples para gerar currículo em PDF a partir de YAML e template LaTeX.
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import shutil
import subprocess
import sys


ROOT = Path(__file__).parent.resolve()

def load_yaml(filepath):
    """Carrega dados do arquivo YAML."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def normalize_url(url):
    """Normaliza URL, adicionando https:// se necessário."""
    if not url:
        return None
    url = str(url).strip()
    if url.startswith(('http://', 'https://')):
        return url
    return f'https://{url}'


def url_display(url):
    """Retorna versão de exibição da URL (sem protocolo)."""
    if not url:
        return None
    url = str(url).strip()
    for prefix in ['https://', 'http://']:
        if url.startswith(prefix):
            return url[len(prefix):]
    return url


def escape_latex(text):
    """Escapa caracteres especiais do LaTeX."""
    if not text:
        return ''
    text = str(text)
    # Caracteres especiais do LaTeX que precisam ser escapados
    special_chars = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '^': r'\textasciicircum{}',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
    }
    for char, escaped in special_chars.items():
        text = text.replace(char, escaped)
    return text


def latex_braces(text):
    """Retorna o texto entre chaves LaTeX."""
    if text is None:
        return ''
    return '{' + str(text) + '}'


def render_template(template_path, data, output_path):
    """Renderiza template Jinja2 e salva em arquivo."""
    
    env = Environment(
        loader=FileSystemLoader(str(ROOT)),
        autoescape=False,
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Adiciona filtros customizados
    env.filters['normalize_url'] = normalize_url
    env.filters['url_display'] = url_display
    env.filters['escape_latex'] = escape_latex
    env.filters['latex_braces'] = latex_braces
    
    template = env.get_template(template_path)
    rendered = template.render(**data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)


def compile_pdf(tex_path, output_dir):
    """Compila LaTeX para PDF usando Tectonic (preferencial) ou latexmk."""
    if shutil.which("tectonic"):
        cmd = ["tectonic", "-o", output_dir, tex_path]
    elif shutil.which("latexmk"):
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", f"-outdir={output_dir}", tex_path]
    else:
        print(
            "Erro: nenhum compilador encontrado.\n"
            "Instale Tectonic (cargo install tectonic) ou TeX Live + latexmk (dnf install texlive-scheme-basic latexmk).",
            file=sys.stderr,
        )
        sys.exit(1)

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    if result.returncode != 0:
        print("Erro ao compilar PDF:", file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)

def main():
    # Cria diretório de saída se não existir
    output_dir = Path('out')

    if output_dir.exists():
        shutil.rmtree(output_dir)
    

    output_dir.mkdir(exist_ok=True)

    
    # Caminhos dos arquivos
    yaml_file = 'cv.yaml'
    template_file = 'template.tex.j2'
    tex_output = output_dir / 'cv.tex'
    pdf_output = output_dir / 'cv.pdf'
    
    # Validações básicas
    if not Path(yaml_file).exists():
        print(f"Erro: arquivo {yaml_file} não encontrado", file=sys.stderr)
        sys.exit(1)
    
    if not Path(template_file).exists():
        print(f"Erro: arquivo {template_file} não encontrado", file=sys.stderr)
        sys.exit(1)
    
    # Carrega dados
    print(f"Carregando dados de {yaml_file}...")
    data = load_yaml(yaml_file)
    
    # Renderiza template
    print(f"Renderizando template {template_file}...")
    render_template(template_file, data, tex_output)
    
    # Compila PDF
    print(f"Compilando PDF...")
    compile_pdf(str(tex_output), str(output_dir))
    
    print(f"✓ PDF gerado com sucesso: {pdf_output}")


if __name__ == '__main__':
    main()
