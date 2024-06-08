var mix = {
	methods: {
		signIn () {
			const username = document.querySelector('#login').value
			const password = document.querySelector('#password').value
			this.postData('/api/sign-in/', {
                username,
                password
            }).then(({data}) => {
				this.access = data.access
				localStorage.setItem('access', this.access)
				localStorage.setItem('username', username)
				// store.commit('setUsername', username)
               	location.assign(`/`)
               	alert('Успешно сохранено')
            }).catch((err) => {
				localStorage.removeItem('access')
				localStorage.removeItem('username')
                console.warn('Ошибка при авторизации')
            })
        }
	},
	mounted() {
	},
	data() {
		return {
			access: '',
			username: ''
		}
	}
}