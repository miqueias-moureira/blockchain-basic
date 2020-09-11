#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 19:29:36 2020

@author: miqueiasmoureira
"""
import json
import datetime
import hashlib
from bottle import route, run

class Blockchain :
    
    def __init__( self ) : 
        self.chain = [] # rede blockchain
        self.create_block( proof = 1, previous_hash = '0' )
        
    def create_block( self, proof, previous_hash ) :
        block = {
                'index' : ( len( self.chain ) + 1 ),
                'timestamp' : str( datetime.datetime.now() ),
                'proof' : proof,
                'previous_hash' : previous_hash
            } # cria um bloco, com index incremental, timestamp de criação, prova de trabalho e o último hash ( link entre blocos )
        self.chain.append( block ) # adiciona na rede 
        return block
    
    def get_block_previous( self ) :
        return self.chain[ -1 ] # retorna o último bloco da rede
    
    def proof_of_work( self, previous_proof ) :
        proof_new = 1 
        while True :
            hash_operation = hashlib.sha256( str( ( proof_new ** 2 ) - ( previous_proof ** 2 ) ).encode() ).hexdigest() # gera um "token" aleatório
            if hash_operation[ : 4 ] == '0000' : # valida se os quatros últimos digitos do token terminam em zeros
                break
            else :
                proof_new += 1 
        return proof_new
                
    def hash( self, block ) :
        encode_block = json.dumps( block, sort_keys = True ).encode() # gera hash do último bloco
        return hashlib.sha256( encode_block ).hexdigest()
    
    def is_chain_valid( self ) :
        previous_index = 0
        for i in self.chain[ 1 : ] :
            if ( i[ 'previous_hash' ] != self.hash( self.chain[ previous_index ] ) ) :
                return False
            hash = hashlib.sha256( str( ( self.chain[ previous_index ][ 'proof' ] ** 2 ) - ( i[ 'proof' ] ** 2 ) ).encode() ).hexdigest()    
            if ( hash[ : 4 ] != '0000' ) :
                return False
            previous_index += 1
        return True
    
    
blockchain = Blockchain()


@route( '/mine_block' )
def mine_block() :
    previous_block = blockchain.get_block_previous()
    proof = blockchain.proof_of_work( previous_block[ 'proof' ] )
    previous_hash = blockchain.hash( previous_block )
    block = blockchain.create_block( proof, previous_hash )
    response = {
            'message' : 'Sucesso, tu criaste um bloco',
            'index' : block[ 'index' ],
            'timestamp' : block[ 'timestamp' ],
            'proof' : block[ 'proof' ],
            'previous_hash' : block[ 'previous_hash' ]
        }
    
    return json.dumps( response )

@route( '/get_chain' )
def get_chain() : 
    response = {
            'chain' : blockchain.chain,
            'length' : len( blockchain.chain )
        } 
    
    return json.dumps( response )

@route( '/is_valid' )
def is_valid() :
    if blockchain.is_chain_valid() :
        response = {
                'message' : 'Blockchain é válido.',
            }
    else :
        response = {
                'message' : 'Blockchain é inválido.',
            }
        
    return json.dumps( response 

run( host = 'localhost', port = 4143 )



                
                
            
