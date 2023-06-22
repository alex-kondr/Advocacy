const form = document.forms[0]

form.addEventListener('submit', async event => {
  event.preventDefault()
  message.innerHTML = "Перевірка"
  const response = await fetch(
    '/login',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: form.username.value,
        password: form.password.value
      })
    }
  )
  result = await response.json()
  console.log("response status", response.status, result)

  if (response.status === 200) {
    console.log("login succesfull")

    localStorage.setItem('access_token', result.access_token)
    window.location = `../news?token=${result.access_token}`
  }
  else if (response.status === 401) {
    message.innerHTML = result.detail
    console.log("login unsuccesfull")
  }
  else {
    message.innerHTML = "Помилка підключення до бази даних"
    console.log("login unsuccesfull")
  }
})


