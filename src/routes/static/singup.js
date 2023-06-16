const form = document.forms[0]
const inputs = document.getElementsByTagName("input")

form.addEventListener('submit', async event => {
    event.preventDefault()

    query = ""
    for (input of inputs) {
        if (!input.required && (input.type == "text" || input.type == "date") && input.value) {
            if (input.name == "phone") {
                query = `${query}&${input.name}=${"%2B" + input.value.slice(1)}`
            }
            else {
                query = `${query}&${input.name}=${input.value}`
            }
        }
    }

    const response = await fetch(
        `https://SilentDismalSweepsoftware.olieksandrkond3.repl.co/api/auth/singup?${query}`,
            {
                method: 'POST',
                body: new FormData(form)
            }
    )

    result = await response.json()
    console.log("response status", response)
    console.log("result: ", result.detail, result)

    if (response.status === 201) {

        form.hidden = true
        detail.innerHTML = result.detail
        buttons.hidden = false
    }
    else {

        form.hidden = true
        buttons.hidden = false
        msg = ""

        for (res of result.detail) {
            msg = msg + res.loc[1] + "-error: " + res.msg + "\n"
        }

        detail.innerHTML = msg + "\n" + result.detail
    }
})


