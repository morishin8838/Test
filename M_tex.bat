@echo off
REM TeXworks��tex���͂������@
REM http://blog.mochiring.net/archives/805
REM 1) �N����A�ҏW����ݒ���J���܂�
REM 2) �^�C�v�Z�b�g�^�u���J���R���p�C���̂��߂̐ݒ�����܂��D
REM 3) �^�C�v�Z�b�g�̕��@�̒ǉ�����
REM 4) �ȉ��̖��ߗ������,bat�Ƃ����g���q�ŕۑ�
REM 5) �V�����^�C�v�Z�b�g��o�^
REM 6) �����́C�o�b�`�t�@�C�������Ŋg���q�������t�@�C������\��$basename���w��
REM
REM

platex -guess-input-enc -interaction=nonstopmode "%1".tex
dvipdfmx -f ptex-ipaex.map "%1".dvi
