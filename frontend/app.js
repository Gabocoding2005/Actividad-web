const API_URL = 'http://localhost:5000/api';

async function addTransaction() {
    const type = document.getElementById('transactionType').value;
    const description = document.getElementById('transactionDescription').value;
    const amount = document.getElementById('transactionAmount').value;

    if (!description || !amount) {
        alert('Por favor completa todos los campos');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: type,
                description: description,
                amount: parseFloat(amount)
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Transacción agregada exitosamente');
            document.getElementById('transactionDescription').value = '';
            document.getElementById('transactionAmount').value = '';
            loadSummary();
        }
    } catch (error) {
        alert('Error al conectar con el servidor: ' + error.message);
    }
}

async function addHabit() {
    const name = document.getElementById('habitName').value;

    if (!name) {
        alert('Por favor ingresa el nombre del hábito');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/habit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('Hábito registrado exitosamente');
            document.getElementById('habitName').value = '';
            loadSummary();
        }
    } catch (error) {
        alert('Error al conectar con el servidor: ' + error.message);
    }
}

async function loadSummary() {
    try {
        const response = await fetch(`${API_URL}/summary`);
        const data = await response.json();

        if (data.success) {
            const summary = data.summary;
            
            document.getElementById('summary').innerHTML = `
                <div><strong>Total Ingresos:</strong> $${summary.total_income.toFixed(2)}</div>
                <div><strong>Total Gastos:</strong> $${summary.total_expense.toFixed(2)}</div>
                <div><strong>Balance:</strong> $${summary.balance.toFixed(2)}</div>
                <div><strong>Transacciones Totales:</strong> ${summary.total_transactions}</div>
                <div><strong>Hábitos Hoy:</strong> ${summary.habits_today}</div>
                <div><strong>Hábitos Totales:</strong> ${summary.total_habits}</div>
            `;

            if (data.recent_transactions.length > 0) {
                document.getElementById('recentTransactions').innerHTML = data.recent_transactions
                    .map(t => `
                        <div>
                            <strong>${t.type === 'income' ? 'Ingreso' : 'Gasto'}:</strong> 
                            ${t.description} - $${t.amount.toFixed(2)} 
                            (${t.date})
                        </div>
                    `).join('');
            } else {
                document.getElementById('recentTransactions').innerHTML = '<p>No hay transacciones</p>';
            }

            if (data.recent_habits.length > 0) {
                document.getElementById('recentHabits').innerHTML = data.recent_habits
                    .map(h => `
                        <div>
                            ${h.name} (${h.date})
                        </div>
                    `).join('');
            } else {
                document.getElementById('recentHabits').innerHTML = '<p>No hay hábitos registrados</p>';
            }
        }
    } catch (error) {
        document.getElementById('summary').innerHTML = 
            '<p style="color: red;">Error al cargar el resumen. Asegúrate de que el servidor esté ejecutándose.</p>';
    }
}

loadSummary();
