# # auth.py
# from authlib.integrations.streamlit_client import OAuth
# import streamlit as st

# def get_oauth():
#     oauth = OAuth()
#     oauth.register(
#         name='google',
#         server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#         client_id='SIZNING_CLIENT_ID',
#         client_secret='SIZNING_CLIENT_SECRET',
#         client_kwargs={'scope': 'openid email profile'}
#     )
#     return oauth
