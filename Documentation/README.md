<center><image src="https://www.pythondiscord.com/static/images/events/summer_code_jam_2024/logo.webp" width="200"></image>

<h1>Credibility Connoisseur</h1>
<h4>Operational Manual</h4>

</center>
<br><br><br><br>



<center>

<h1>THIS DOCUMENT WILL OUTLINE THE BASIC REQUIREMENTS TO ENSURE CREDIBILITY CONNOISSEUR OPERATES.</h1>

</center>

<center><blockquote><h3>Attention!</h3><br> There is the risk of the bot failing to operate with some questions, due to malformed question input, this was due to us running out of coding time. If this occurs, please rerun the bot. We are sorry for the inconviences this causes.</blockquote></center>


<br><br><br><br>
<br><br><br><br>
<h1>How to Start</h1>
<ol>
<li> The bot setup is pretty straight forward, and should take a maximum of 10 minutes. Take a look at the <a href="https://github.com/KRSpinelli/blissful-blazars-project/blob/c815c57947d118347ab21490c20a093c85d3debd/requirements-dev.txt">dependencies</a>.
<blockquote> You may need to manually run the following, due to issues with this specific dependency:<br><code>pip install discord-py-interactions</code></blockquote></li>
<li>Once installed, go to <a href="https://github.com/KRSpinelli/blissful-blazars-project/blob/c815c57947d118347ab21490c20a093c85d3debd/config.py">config.py</a> and enter your bots token, and the guild ID.
<blockquote>Keep your Token Secret!</blockquote></li>
<li>Lastly, run the main.py file within the main directory, your bot should state in the console output that the quiz cog is loaded.</li>

</ol>


Commands: 

<code>/start</code> - Starts the game. Will throw an exception if an active game is present. <br> 
<code>/leaderboard></code> - Returns an embed of all game scores for a user combined, alongside all other users total scores.


<center><img src="https://i.imgur.com/9uxKhB2.png"></center>



