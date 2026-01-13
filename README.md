# Gerador de Currículo em PDF

Gerador simples de currículo em PDF usando YAML, Jinja2 e LaTeX.

## Requisitos

- Python 3.6+
- Tectonic (compilador LaTeX)
- Bibliotecas Python: `pyyaml`, `jinja2`

## Instalação

```bash
# Instalar dependências Python
pip install pyyaml jinja2

# Instalar Tectonic (Fedora)
sudo dnf install tectonic
```

## Uso

1. Edite `cv.yaml` com seus dados
2. Execute:
   ```bash
   python build.py
   ```
3. O PDF será gerado em `out/cv.pdf`

## Estrutura

- `cv.yaml` - Dados do currículo em YAML
- `template.tex.j2` - Template LaTeX com Jinja2
- `build.py` - Script de build
- `out/` - Diretório de saída (gerado automaticamente)

## Personalização

- Edite `cv.yaml` para atualizar seus dados
- Edite `template.tex.j2` para ajustar o layout LaTeX
