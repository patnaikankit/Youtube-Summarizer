// here we are trying the check the link provided by the user and send it for further processing
// if the link is valid we will extract the transcript and pass it the gpt api for the genearting the summary
document.getElementById('button').addEventListener('click', async () => {
    const link = document.getElementById('link').value;
    const summary = document.getElementById('summary');
    if(link){
        document.getElementById('loading-circle').style.display = 'block';
        summary.innerHTML = ''; 
        const endpointUrl = '/genarate-summary';  
        // once we have the link we will provide that to a specified route where the rest of the task can be done
        try{
            const response = await fetch(endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: link })
            });
            const data = await response.json();
            summary.innerHTML = data.content;
        } 
        catch(error){
            console.error("Error occurred:", error);
            alert("Something went wrong. Please try again later.");
        }
        document.getElementById('loading-circle').style.display = 'none';
    } 
    else{
        alert("Please enter a valid YouTube link.");
    }
});