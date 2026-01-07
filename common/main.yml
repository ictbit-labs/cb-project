---
- name: Deploy and Sync Configuration
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    # 1. SETUP: Define your paths and stack name
    stack_name: "MY-COMPANY-STACK-NAME"  # <--- REPLACE THIS with the real Stack Name in AWS
    common_vars_file: "vars/common.yml"
    project_root: "../my-repo"
    venv_path: "../my-repo/.venv"

  tasks:
    # ----------------------------------------------------------------
    # 1. DEPLOY (Using your company's custom tool)
    # ----------------------------------------------------------------
    - name: Run Custom Deployment
      ansible.builtin.shell: |
        source .venv/bin/activate
        # Replace this with the actual command you run manually
        python3 deploy_wrapper.py 
      args:
        chdir: "{{ project_root }}"
        executable: /bin/bash

    # ----------------------------------------------------------------
    # 2. FETCH (Query AWS CloudFormation directly)
    # ----------------------------------------------------------------
    - name: Get Stack Outputs from AWS
      ansible.builtin.command: >
        aws cloudformation describe-stacks 
        --stack-name {{ stack_name }} 
        --query "Stacks[0].Outputs" 
        --output json
      register: aws_output
      changed_when: false

    # ----------------------------------------------------------------
    # 3. TRANSFORM (Convert List to Dictionary)
    # AWS returns: [{'OutputKey': 'A', 'OutputValue': 'B'}]
    # We want: {'A': 'B'}
    # ----------------------------------------------------------------
    - name: Parse AWS Outputs
      ansible.builtin.set_fact:
        stack_outputs: "{{ aws_output.stdout | from_json | items2dict(key_name='OutputKey', value_name='OutputValue') }}"

    # ----------------------------------------------------------------
    # 4. MAP (Connect AWS Outputs to Your Variables)
    # ----------------------------------------------------------------
    - name: Map Outputs to Config Variables
      ansible.builtin.set_fact:
        vars_to_update:
          # common.yml Key       : AWS Output Key
          organization_id:         "{{ stack_outputs['OrganizationId'] }}"
          security_account_id:     "{{ stack_outputs['SecurityAccountId'] }}"
          vpc_id:                  "{{ stack_outputs['VpcId'] }}"

    # ----------------------------------------------------------------
    # 5. UPDATE (Run the Python Script)
    # ----------------------------------------------------------------
    - name: Update common.yml file
      ansible.builtin.command:
        argv:
          - "{{ venv_path }}/bin/python3"
          - "roles/common/files/update_config.py"
          - "--target"
          - "{{ common_vars_file }}"
          - "--data"
          - "{{ vars_to_update | to_json }}"

    - name: Done
      ansible.builtin.debug:
        msg: "✅ common.yml updated! Next playbook is ready to run."
