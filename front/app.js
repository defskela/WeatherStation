import { CONNECTION_DATA } from './security.js';

const socket = new WebSocket(CONNECTION_DATA);

// Получаем элементы HTML для отображения данных
const temperatureEl = document.getElementById('temperature');
const humidityEl = document.getElementById('humidity');
const pressureEl = document.getElementById('pressure');
const co2_1El = document.getElementById('co2_1');
const co2_2El = document.getElementById('co2_2');
const ppbEl = document.getElementById('ppb');

// Обработка события открытия соединения
socket.addEventListener('open', () => {
	console.log('WebSocket соединение открыто');
});

// Обработка входящих сообщений
socket.addEventListener('message', (event) => {
	console.log('Получены данные: ', event.data);
	try {
		const data = JSON.parse(event.data);

		// Обновляем данные на экране
		temperatureEl.textContent = data.temperature;
		humidityEl.textContent = data.humidity;
		pressureEl.textContent = data.pressure;
		co2_1El.textContent = data.co2;
		co2_2El.textContent = data.co2eq;
		ppbEl.textContent = data.tvoc;
	} catch (error) {
		console.error('Ошибка обработки данных: ', error);
	}
});

// Обработка закрытия соединения
socket.addEventListener('close', () => {
	console.log('WebSocket соединение закрыто');
});

// Обработка ошибок
socket.addEventListener('error', (error) => {
	console.error('WebSocket ошибка: ', error);
});
