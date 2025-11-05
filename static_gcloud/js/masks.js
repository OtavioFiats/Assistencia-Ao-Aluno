// Função para aplicar máscara de telefone
function maskPhone(event) {
    let input = event.target;
    let value = input.value.replace(/\D/g, ''); // Remove tudo que não é número
    let formattedValue = '';

    if (value.length <= 11) {
        // Formata como (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        if (value.length > 2) {
            formattedValue += '(' + value.substring(0, 2) + ') ';
            if (value.length > 7) {
                formattedValue += value.substring(2, 7) + '-';
                formattedValue += value.substring(7, 11);
            } else if (value.length > 6) {
                formattedValue += value.substring(2, 6) + '-';
                formattedValue += value.substring(6, value.length);
            } else {
                formattedValue += value.substring(2, value.length);
            }
        } else {
            formattedValue = value;
        }
    }

    input.value = formattedValue;
}

// Função para inicializar as máscaras
document.addEventListener('DOMContentLoaded', function() {
    // Aplica máscara nos campos de telefone
    const phoneFields = document.querySelectorAll('input[name="fone"]');
    phoneFields.forEach(field => {
        field.addEventListener('input', maskPhone);
        field.setAttribute('maxlength', '15'); // (XX) XXXXX-XXXX = 15 caracteres
        field.setAttribute('placeholder', '(XX) XXXXX-XXXX');
    });
});