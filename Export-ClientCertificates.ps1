<# Export all user certificates from the FNMT as PFX with 12345 as password, run this from a console:

$ powershell -exec bypass .\Export-ClientCertificates.ps1

Lots of times certificates are not allowed to export the private key, you can use the jailbreak program from 
https://github.com/iSECPartners/jailbreak to bypass it, copy this script in the same folder as the jaibreak/binaries and run as
$ jailbreak64.exe powershell -exec bypass ..\Export-ClientCertificates.ps1

to import all at the same time create a file called ImportAllPFX.ps1 and put inside:
------------------------------------
$pfX = Get-ChildItem *.pfx
$pwd = ConvertTo-SecureString -String "12345" -AsPlainText -Force

ForEach ($cert in $pfx){
    
    Import-PfxCertificate -Password $pwd -FilePath $cert -CertStoreLocation Cert:\CurrentUser\My -Exportable
    }
-------------------------------------
#>


param(
    [Parameter(Mandatory = $false)]
    [String]$Password = "12345"
    )
    
$passwd = ConvertTo-SecureString -String $Password -Force -AsPlainText

$certPath = "Cert:\CurrentUser\My"

# first IF ? If it's a certificate seconf IF ? it's from the FNMT (spanish cert authority) remove if you don't need it
$cert = Get-ChildItem $certPath -Recurse | ? { $_ -is [System.Security.Cryptography.X509Certificates.X509Certificate2] } |  ? {$_.Issuer -eq "CN=AC FNMT Usuarios, OU=Ceres, O=FNMT-RCM, C=ES" }


Foreach ( $cer in $cert ) {
    write-host $cer.SubjectName.Name
    $certSubjectName = $cer.SubjectName.Name

    if ($cer.SubjectName.Name -match "CN=(?<commonName>[^,]*)") {
            
        $certCommonName = $Matches['commonName']
        $certThumbprint = $cer.Thumbprint

        
        # export it to the parent directory remove (".." + ) if not
        $exportFile = "..\" + "$certCommonName ($certThumbprint).pfx"


        $cer | Export-PfxCertificate -FilePath  $exportFile -Password $passwd -ChainOption BuildChain
        }
    }
