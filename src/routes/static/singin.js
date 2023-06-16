const form = document.forms[0]

form.addEventListener('submit', async event => {
  event.preventDefault()
  const response = await fetch(
    'https://SilentDismalSweepsoftware.olieksandrkond3.repl.co/api/auth/login',
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
    localStorage.setItem('refresh_token', result.refresh_token)    
    window.location = '../contacts'
  }
  else if (response.status === 401) {
    message.innerHTML = result.detail
    message.hidden = false
  }

})


