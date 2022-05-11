mkdir -p decrypted_sally_documents/cancer_cells/
for file in encrypted_sally_documents/*.encrypted; do python decrypt_files.py ${file} -o decrypted_sally_documents/; done
for file in encrypted_sally_documents/cancer_cells/*.encrypted; do python decrypt_files.py ${file} -o decrypted_sally_documents/cancer_cells/; done

