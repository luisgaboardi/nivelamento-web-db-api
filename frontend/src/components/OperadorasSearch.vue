<template>
    <div class="operadoras-search">
        <h1>Busca de Operadoras</h1>
        <input type="text" v-model="termo" placeholder="Digite o termo de busca" @keyup.enter="buscarOperadoras" />
        <button @click="buscarOperadoras">Buscar</button>

        <div v-if="loading">Carregando...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <table v-if="operadoras.length > 0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Registro ANS</th>
                    <th>CNPJ</th>
                    <th>Razão Social</th>
                    <th>Nome Fantasia</th>
                    <th>Modalidade</th>
                    <th>Cidade</th>
                    <th>UF</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="operadora in operadoras" :key="operadora.id">
                    <td>{{ operadora.id }}</td>
                    <td>{{ operadora.registro_ans }}</td>
                    <td>{{ operadora.cnpj }}</td>
                    <td>{{ operadora.razao_social }}</td>
                    <td>{{ operadora.nome_fantasia }}</td>
                    <td>{{ operadora.modalidade }}</td>
                    <td>{{ operadora.cidade }}</td>
                    <td>{{ operadora.uf }}</td>
                </tr>
            </tbody>
        </table>

        <div v-if="operadoras.length === 0 && !loading && !error">
            Nenhuma operadora encontrada.
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            termo: "",
            operadoras: [],
            loading: false,
            error: null,
        };
    },
    methods: {
        async buscarOperadoras() {
            if (this.termo.length < 3) {
                this.error = "O termo de busca deve ter pelo menos 3 caracteres.";
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get(
                    `http://127.0.0.1:8000/operadoras/busca`,
                    {
                        params: { termo: this.termo },
                    }
                );
                this.operadoras = response.data.data;
            } catch (err) {
                this.error = "Erro ao buscar operadoras. Tente novamente mais tarde.";
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<style scoped>
.operadoras-search {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

input {
    padding: 8px;
    width: 300px;
    margin-right: 10px;
}

button {
    padding: 8px 16px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
}

.error {
    color: red;
    margin-top: 10px;
}
</style>