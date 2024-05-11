import { useState } from 'react'

import { Grid, Typography,Link, Button } from '@mui/material'

import './App.css'

interface VoterInfo{
  private_key: string,
  president: string,
  senator: string
}

function App() {
  const [senator, setSenator] = useState("")
  const [president, setPresident] = useState("")
  
  async function dispense(){
    const voter_info_response = await fetch("/dispense_voter_info")
    const voter_info: VoterInfo = await voter_info_response.json()
    setPresident(voter_info.president)
    setSenator(voter_info.senator)
    const private_key = new Blob([JSON.stringify({"private":voter_info.private_key})],{ type: "application/json" })
    const private_key_link = URL.createObjectURL(private_key)
    const temp_anchor = document.createElement('a');
    temp_anchor.href = private_key_link
    temp_anchor.download = "private.json"
    document.body.appendChild(temp_anchor)
    temp_anchor.click()
    document.body.removeChild(temp_anchor)
  }

  return (
    <Grid container rowSpacing={4}>

    <Grid item xs={12}>
    <Typography variant="h5" component="h5"> 
    Click or tap the "GENERATE" Button below to receive your voting key and your voting instructions.
    </Typography>
    </Grid>

    <Grid item xs={12}>
    <Button variant="contained" onClick={dispense}>Generate</Button>
    </Grid>
    
    <Grid item xs={12}>
      Vote for this President: {president}
    </Grid>

    <Grid item xs={12}>
      Vote for this Senator: {senator}
    </Grid>

    <Grid item xs={12}>
      <Typography variant="h6" component ="h6">
      If you have finished downloading your voting key and reviewing the instructions above, you may now visit 
      </Typography>
      
      <Link href="https://neweboto.xyz:43192">
      <Typography variant="h6" component="h6">the eBoto website</Typography>
      </Link>
      
      <Typography variant="h6" component="h6">
      When you visit the login page of the eBoto site, click "Browse...", select the private.json that was downloaded after you tapped or clicked "Generate" on this site, and choose "LOG IN AS VOTER".
      </Typography>

    </Grid>

    <Grid item xs={12}>
      <Link href="https://neweboto.xyz:43192/dispenser/license.txt">
      <Typography variant="body2" component="h6">
        License Text
      </Typography>
      </Link>
    </Grid>

    </Grid>
  )
}

export default App
