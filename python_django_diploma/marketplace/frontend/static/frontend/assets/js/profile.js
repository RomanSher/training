var mix = {
    methods: {
        getProfile() {
            this.getData(`/api/profile/`).then(data => {
                this.fullName = data.full_name
                this.avatar = data.avatar
                this.phone = data.phone
                this.email = data.email
            }).catch(() => {
                console.warn('Ошибка при получении профиля')
            })
        },
        changeProfile () {
            if(!this.fullName.trim().length || !this.phone.trim().length || !this.email.trim().length) {
                alert('В форме присутствуют незаполненные поля')
                return
            }
            if (this.phone.charAt(0) !== '+') {
                this.phone = '+' + this.phone;
            }
            this.updateData('/api/profile/', {
                full_name: this.fullName,
                phone: this.phone,
                email: this.email
            }).then(({data}) => {
                this.fullName = data.full_name
                this.phone = data.phone
                this.email = data.email
               alert('Успешно сохранено')
            }).catch(() => {
                console.warn('Ошибка при обновлении профиля')
            })
        },
        changePassword () {
            if (
                !this.passwordCurrent.trim().length ||
                !this.password.trim().length ||
                !this.passwordReply.trim().length ||
                this.password !== this.passwordReply
            ) {
                alert('В форме присутствуют незаполненные поля или пароли не совпадают')
                return
            }
            this.updateData('/api/profile/password/', {
                password_current: this.passwordCurrent,
                password: this.password,
                password_reply: this.passwordReply
            }).then(({data}) => {
                alert('Успешно сохранено')
                this.passwordCurrent = ''
                this.password = ''
                this.passwordReply = ''
            }).catch(() => {
                console.warn('Ошибка при сохранении пароля')
            })
        },
        setAvatar (event) {
            const target = event.target
            const file = target.files?.[0] ?? null
            if (!file) return

            const formData = new FormData()
            formData.append('avatar', file)

            this.updateData('/api/profile/avatar/', formData, {'Content-Type': 'multipart/form-data'})
                .then(({data}) => {
                    this.avatar = data.avatar
                }).catch(() => {
                     console.warn('Ошибка при обновлении изображения')
                })
        },
        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        clearAvatar() {
            this.avatar = null
        }
    },
    created() {
        this.getProfile();
    },
    data() {
        return {
            username: '',
            fullName: null,
            phone: null,
            email: null,
            avatar: null,
            password: '',
            passwordCurrent: '',
            passwordReply: ''
        }
    },
}