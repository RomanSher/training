var mix = {
	methods: {
		getOrder(orderId) {
			if(typeof orderId !== 'number') return
			this.getData(`/api/orders/${this.orderId}/`)
				.then(data => {
					this.orderId = data.id
					this.createdAt = data.created_at
					this.fullName = data.full_name
					this.phone = data.phone
					this.email = data.email
					this.deliveryType = data.delivery_type
					this.city = data.city
					this.address = data.address
					this.paymentType = data.payment_type
					this.status = data.status
					this.totalCost = data.total_cost
					this.products = data.products
					if (typeof data.paymentError !== 'undefined') {
						this.paymentError = data.paymentError
					}
				})
		},
		confirmOrder() {
			if (this.orderId !== null) {
				const data = {
					...this,
					full_name: this.fullName,
					phone: this.formattedPhone,
					delivery_type: this.deliveryType,
					payment_type: this.paymentType
				};
				delete data.fullName;
				delete data.deliveryType;
				delete data.paymentType;
				this.updateData(`/api/orders/${this.orderId}/`, data)
					.then(({ data: { id } }) => {
						alert('Заказ подтвержден')
						location.replace(`/payment/${id}/`)
					})
					.catch(() => {
						console.warn('Ошибка при подтверждения заказа')
					})
			}
		},
		auth() {
			const username = document.querySelector('#username').value
			const password = document.querySelector('#password').value
			this.postData('/api/sign-in/', {
                username,
                password
				}).then(({ data, status }) => {
					localStorage.setItem('access', data.access)
					localStorage.setItem('username', username)
					location.assign(`/order/${this.orderId}`)
					alert('Успешно сохранено')
				})
				.catch(() => {
					localStorage.removeItem('access')
					localStorage.removeItem('username')
					alert('Ошибка авторизации')
				})
		}
	},
	mounted() {
		if(location.pathname.startsWith('/order/')) {
			const orderId = location.pathname.replace('/order/', '').replace('/', '')
			this.orderId = orderId.length ? Number(orderId) : null
			this.getOrder(this.orderId);
		}
	},
	computed: {
		totalCostDelivery() {
			this.totalCostWithDelivery = this.totalCost
			if (this.deliveryType && this.totalCost) {
				if (this.deliveryType === 'EXPRESS') {
					this.totalCostWithDelivery += 500;
				} else if (this.deliveryType === 'ORDINARY') {
					if (this.totalCost < 2000) {
						this.totalCostWithDelivery += 200;
					}
				}
			}
			return this.totalCostWithDelivery;
		},
		formattedPhone() {
			if (this.phone.charAt(0) !== '+') {
                this.phone = '+' + this.phone;
            }
		}
	},
	data() {
		return {
			createdAt: null,
			fullName: null,
			phone: null,
			email: null,
			deliveryType: null,
			city: null,
			address: null,
			paymentType: null,
			status: null,
			totalCost: null,
			products: [],
			paymentError: null,
			totalCostWithDelivery: null
		}
	},
}