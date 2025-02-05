document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('name-form');
    const nameInput = document.getElementById('name-input');
    const resultDiv = document.getElementById('result');
    const countriesList = document.getElementById('countries-list');

    // Обработчик отправки формы
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Предотвращаем перезагрузку страницы

        // Очищаем предыдущие результаты
        countriesList.innerHTML = '';
        resultDiv.classList.add('hidden');

        // Получаем имя из input
        const name = nameInput.value.trim();
        if (!name) {
            alert('Пожалуйста, введите имя.');
            return;
        }

        try {
            // Отправляем GET запрос к API
            const response = await fetch(`/api/v1/names/?name=${encodeURIComponent(name)}`);
            if (!response.ok) {
                throw new Error('Ошибка при получении данных.');
            }

            // Парсим JSON ответ
            const data = await response.json();

            // Проверяем, есть ли данные о странах
            if (!data.country || data.country.length === 0) {
                alert('Данные не найдены.');
                return;
            }

            // Отображаем результаты
            resultDiv.classList.remove('hidden');
            data.country.forEach(country => {
                const li = document.createElement('li');
                li.textContent = `${country.country_id}: ${country.probability}`;
                countriesList.appendChild(li);
            });
        } catch (error) {
            console.error(error);
            alert('Произошла ошибка при получении данных.');
        }
    });
});