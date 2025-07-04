from flask import Blueprint, request, jsonify
from git import Repo

from server.antipatterns.blob import is_blob_antipattern_to_json
from server.antipatterns.spaghetti_code import is_spaghetti_code_to_json
from server.antipatterns.swiss_army_knife import is_sak_to_json

import os
import json
import tempfile
import shutil
import stat

antipyttern_bp = Blueprint('antipyttern', __name__)
TEMP_FOLDER = 'tmp'


def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def analyze_python_files(project_path, file_paths, pattern):
    results = {}

    if pattern in ['blob', 'all']:
        results['blob'] = [json.loads(is_blob_antipattern_to_json(p)) for p in file_paths]

    if pattern in ['spaghetti', 'all']:
        results['spaghetti'] = [
            json.loads(is_spaghetti_code_to_json(project_path, p)) for p in file_paths
        ]

    if pattern in ['sak', 'all']:
        results['sak'] = [
            json.loads(is_sak_to_json(project_path, p)) for p in file_paths
        ]

    return results


@antipyttern_bp.route('/scan_files', methods=['POST'])
def scan_files():
    uploaded_files = request.files.getlist('files')
    pattern = request.args.get('pattern', default='all').lower()
    print(pattern)

    if not uploaded_files:
        return jsonify({'error': 'No files received'}), 400

    temp_dir = tempfile.mkdtemp()
    file_paths = []

    for f in uploaded_files:
        if not f.filename.endswith('.py'):
            continue
        path = os.path.join(temp_dir, f.filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f.save(path)
        file_paths.append(path)

    results = analyze_python_files(temp_dir, file_paths, pattern)
    shutil.rmtree(temp_dir)

    return jsonify({
        'status': 'success',
        'file_count': len(uploaded_files),
        'message': 'Files uploaded and analyzed successfully.',
        'results': results
    }), 200


@antipyttern_bp.route('/scan_repo', methods=['POST'])
def scan_repo():
    data = request.get_json()
    repo_url = data.get('repo_url')
    pattern = request.args.get('pattern', default='all').lower()
    print(pattern)

    if not repo_url:
        return jsonify({'error': 'Missing GitHub repository URL'}), 400

    temp_dir = tempfile.mkdtemp()
    repo_dir = os.path.join(temp_dir, 'repo')

    try:
        Repo.clone_from(repo_url, repo_dir)
    except Exception as e:
        shutil.rmtree(temp_dir)
        return jsonify({'error': f'Failed to clone repository: {str(e)}'}), 500

    file_paths = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                file_paths.append(os.path.join(root, file))
    results = analyze_python_files(repo_dir, file_paths, pattern)

    shutil.rmtree(temp_dir, onerror=handle_remove_readonly)

    return jsonify({
        'status': 'success',
        'file_count': len(file_paths),
        'message': 'Repository analyzed successfully.',
        'results': results
    }), 200
