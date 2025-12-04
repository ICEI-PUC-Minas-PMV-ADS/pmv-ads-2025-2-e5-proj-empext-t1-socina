<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Gestão - Socina</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body { background-color: #f4f6f9; }
        .card-resumo {
            border-left: 5px solid;
            transition: transform 0.2s;
        }
        .card-resumo:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .icon-bg {
            font-size: 2.5rem;
            opacity: 0.2;
            position: absolute;
            right: 15px;
            bottom: 10px;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-dark bg-dark mb-4">
  <div class="container-fluid">
    <span class="navbar-brand mb-0 h1">SOCINA - Painel de Gestão</span>
    <div class="d-flex gap-2">
        <a href="/admin/" class="btn btn-warning btn-sm">Painel Admin (Categorias)</a>
        <a href="{% url 'home' %}" class="btn btn-outline-light btn-sm">Sair</a>
    </div>
  </div>
</nav>

<div class="container">
    
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body d-flex gap-2 flex-wrap justify-content-center">
                    <a href="{% url 'cadastra_produto' %}" class="btn btn-success btn-lg">➕ Novo Produto</a>
                    <a href="{% url 'lista_produtos' %}" class="btn btn-primary btn-lg">📦 Meus Produtos</a>
                    <a href="/admin/loja/categoria/" class="btn btn-info btn-lg text-white">🏷️ Criar Categorias</a>
                    <a href="{% url 'exportar_relatorio_csv' %}" class="btn btn-secondary btn-lg">📥 Baixar Relatório</a>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-3 mb-4">
        <div class="col-md-4">
            <div class="card card-resumo h-100 border-success text-success p-3">
                <h5 class="card-title text-uppercase text-muted small">Faturamento Total</h5>
                <h2 class="display-6 fw-bold">R$ {{ total_vendas_valor|floatformat:2 }}</h2>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card card-resumo h-100 border-info text-info p-3">
                <h5 class="card-title text-uppercase text-muted small">Vendas Concluídas</h5>
                <h2 class="display-6 fw-bold">{{ total_vendas_qtd }}</h2>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card card-resumo h-100 border-warning text-warning p-3">
                <h5 class="card-title text-uppercase text-muted small">Total de Pedidos</h5>
                <h2 class="display-6 fw-bold">{{ total_pedidos }}</h2>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <h5 class="mb-0">Vendas por Mês</h5>
                </div>
                <div class="card-body">
                    <canvas id="salesChart" height="80"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    const labels = JSON.parse('{{ chart_labels|safe }}');
    const data = JSON.parse('{{ chart_data|safe }}');

    new Chart(document.getElementById('salesChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Faturamento (R$)',
                data: data,
                backgroundColor: '#0d6efd'
            }]
        }
    });
</script>

</body>
</html>