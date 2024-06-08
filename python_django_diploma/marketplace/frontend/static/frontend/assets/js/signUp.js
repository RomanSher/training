var mix = {
	methods: {
		signUp () {
			const full_name = document.querySelector('#fullName').value
			const username = document.querySelector('#login').value
			const email = document.querySelector('#email').value
			const password = document.querySelector('#password').value
			const password2 = document.querySelector('#password2').value
			this.postData('/api/sign-up/', {
			    full_name,
                username,
                email,
                password,
                password2
            }).then(() => {
				alert('Успешно сохранено');
			}).catch(() => {
				console.warn('Ошибка при регистрации');
			})
		}
	}
}