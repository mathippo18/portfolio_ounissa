import paramiko
from flask import jsonify, Response

# Extensions vidéo autorisées
VALID_EXT = {".mp4", ".mov", ".webm", ".m4v"}

# Configuration SFTP
SFTP_HOST = "m-poinsot.com"
SFTP_PORT = 22
SFTP_USER = "ounissa"
SFTP_PASS = r'c;v,5ZjUAp~1W!G"y&ng:<7[Ua)C5x-9-fA@-5,QnCBP%G\1>gDMfP;bw6gz\AH57\L1%q/u&bwW;f[AuLe$B}Yf[dX_UbzS<_q'
SFTP_ROOT = "videos"

def get_sftp_connection():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return transport, sftp

def list_videos():
    output = []
    try:
        transport, sftp = get_sftp_connection()
        for folder_attr in sftp.listdir_attr(SFTP_ROOT):
            folder_name = folder_attr.filename
            folder_path = f"{SFTP_ROOT}/{folder_name}"
            try:
                files = sftp.listdir(folder_path)
            except IOError:
                continue
            videos = [f for f in files if f.lower().endswith(tuple(VALID_EXT))]
            if videos:
                output.append({"folder": folder_name, "videos": videos})
        sftp.close()
        transport.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not output:
        return jsonify({"error": "Aucune vidéo trouvée"}), 404
    return jsonify(output)

def stream_video(folder, filename):
    try:
        transport, sftp = get_sftp_connection()
        sftp_path = f"{SFTP_ROOT}/{folder}/{filename}"
        try:
            sftp.stat(sftp_path)
        except FileNotFoundError:
            sftp.close()
            transport.close()
            return "Fichier non trouvé", 404

        def generate():
            with sftp.open(sftp_path, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk:
                        break
                    yield chunk
            sftp.close()
            transport.close()

        # Type MIME
        if filename.lower().endswith(".mp4"):
            mimetype = "video/mp4"
        elif filename.lower().endswith(".webm"):
            mimetype = "video/webm"
        elif filename.lower().endswith(".mov"):
            mimetype = "video/quicktime"
        else:
            mimetype = "application/octet-stream"

        return Response(generate(), mimetype=mimetype)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
