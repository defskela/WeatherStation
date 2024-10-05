const socket = new WebSocket('ws://localhost:8766');

socket.onmessage = function (event) {
	console.log('Data from sensor:', event.data);
	// Логика отображения данных на странице
};
// Подключаемся к WebSocket
// const socket = new WebSocket(socketUrl);

// Получаем элементы HTML для отображения данных
const temperatureEl = document.getElementById('temperature');
const humidityEl = document.getElementById('humidity');
const pressureEl = document.getElementById('pressure');
const co2_1El = document.getElementById('co2_1');
const co2_2El = document.getElementById('co2_2');
const ppbEl = document.getElementById('ppb');

// Обработка события открытия соединения
// socket.addEventListener('open', () => {
// 	console.log('WebSocket соединение открыто');
// });

// // Обработка входящих сообщений
// socket.addEventListener('message', (event) => {
// 	try {
// 		const data = JSON.parse(event.data);

// 		// Обновляем данные на экране
// 		temperatureEl.textContent = data.temp;
// 		humidityEl.textContent = data.hum;
// 		pressureEl.textContent = data.pres;
// 		co2_1El.textContent = data.co2;
// 		co2_2El.textContent = data.co2_eq;
// 		ppbEl.textContent = data.ppb;
// 	} catch (error) {
// 		console.error('Ошибка обработки данных: ', error);
// 	}
// });

// // Обработка закрытия соединения
// socket.addEventListener('close', () => {
// 	console.log('WebSocket соединение закрыто');
// });

// // Обработка ошибок
// socket.addEventListener('error', (error) => {
// 	console.error('WebSocket ошибка: ', error);
// });
