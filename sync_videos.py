import os
import paramiko

# Configuration SFTP
SFTP_HOST = "m-poinsot.com"
SFTP_PORT = 22
SFTP_USER = "ounissa"
SFTP_PASS = r'c;v,5ZjUAp~1W!G"y&ng:<7[Ua)C5x-9-fA@-5,QnCBP%G\1>gDMfP;bw6gz\AH57\L1%q/u&bwW;f[AuLe$B}Yf[dX_UbzS<_q'  # chaîne brute pour les backslashes
SFTP_ROOT = "/videos"

# Dossier local où copier les vidéos
LOCAL_ROOT = "static/videos"

# Extensions vidéo autorisées
VALID_EXT = {".mp4", ".mov", ".webm", ".m4v"}

def get_sftp_connection():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return transport, sftp

def download_folder(sftp, remote_folder, local_folder):
    os.makedirs(local_folder, exist_ok=True)
    for item in sftp.listdir_attr(remote_folder):
        remote_path = f"{remote_folder}/{item.filename}"
        local_path = os.path.join(local_folder, item.filename)
        if stat.S_ISDIR(item.st_mode):
            # Dossier → appel récursif
            download_folder(sftp, remote_path, local_path)
        elif any(item.filename.lower().endswith(ext) for ext in VALID_EXT):
            # Fichier vidéo → télécharger
            print(f"Téléchargement : {remote_path} → {local_path}")
            sftp.get(remote_path, local_path)

def main():
    try:
        transport, sftp = get_sftp_connection()
        download_folder(sftp, SFTP_ROOT, LOCAL_ROOT)
        sftp.close()
        transport.close()
        print("Synchronisation terminée !")
    except Exception as e:
        print("Erreur :", e)

if __name__ == "__main__":
    import stat
    main()
