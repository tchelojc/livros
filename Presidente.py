import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import ast
from functools import lru_cache
import requests
import time
import math
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="FLUX-ON Leitura Quântica",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS AVANÇADOS ---
st.markdown("""
<style>
    /* Tema principal aprimorado */
    .main {
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e);
        color: #e6e6fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Tipografia moderna */
    h1, h2, h3, h4, h5, h6 {
        color: #e0aaff;
        font-family: 'Georgia', serif;
        text-shadow: 0 0 15px rgba(224, 170, 255, 0.4);
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #e0aaff, #9d4edd, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 3px solid #7b2cbf;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Cards e containers futuristas */
    .metric-card {
        background: rgba(45, 45, 65, 0.8);
        border-left: 5px solid #9d4edd;
        padding: 20px;
        margin: 15px 0;
        border-radius: 15px;
        box-shadow: 0 6px 25px rgba(157, 78, 221, 0.3);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        border: 1px solid rgba(157, 78, 221, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(157, 78, 221, 0.4);
        border-color: rgba(157, 78, 221, 0.4);
    }
    
    /* Text area styling aprimorado */
    .text-container {
        background: rgba(30, 30, 46, 0.95);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #7b2cbf;
        box-shadow: 0 0 40px rgba(123, 44, 191, 0.25);
        backdrop-filter: blur(8px);
        line-height: 1.9;
        font-size: 17px;
        max-height: 600px;
        overflow-y: auto;
        font-family: 'Georgia', serif;
    }
    
    /* Highlight styles melhorados */
    .highlight {
        background: linear-gradient(120deg, #9d4edd50, #5a189a70);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #e0aaff;
        font-weight: 600;
        color: #f8f9fa;
    }
    
    .highlight-important {
        background: linear-gradient(120deg, #ff6b6b50, #ee5a2470);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #ff6b6b;
        font-weight: 700;
        color: #f8f9fa;
    }
    
    .user-highlight {
        background: linear-gradient(120deg, #4cc9f050, #4895ef70);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #4cc9f0;
        font-weight: 600;
        color: #f8f9fa;
    }
    
    /* Botões de navegação quântica */
    .nav-button {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        color: white;
        border: none;
        padding: 14px 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.3);
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #7b2cbf, #5a189a);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(157, 78, 221, 0.5);
    }
    
    /* Sidebar quântica */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 3px solid #9d4edd;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Abas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: rgba(45, 45, 65, 0.7);
        border-radius: 10px 10px 0 0;
        gap: 10px;
        padding: 10px 20px;
        border-bottom: 2px solid #7b2cbf;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        color: white;
    }
    
    /* Barras de progresso quânticas */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9d4edd, #5a189a);
        box-shadow: 0 0 10px rgba(157, 78, 221, 0.5);
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetric"] {
        background: rgba(45, 45, 65, 0.8);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #9d4edd;
        box-shadow: 0 4px 20px rgba(157, 78, 221, 0.2);
    }
    
    /* Animações suaves */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 3s infinite;
    }
    
    /* Scrollbar personalizada */
    .text-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .text-container::-webkit-scrollbar-track {
        background: rgba(30, 30, 46, 0.5);
        border-radius: 10px;
    }
    
    .text-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        border-radius: 10px;
    }
    
    /* Efeitos de foco */
    .focus-effect {
        transition: all 0.3s ease;
    }
    
    .focus-effect:hover {
        box-shadow: 0 0 25px rgba(157, 78, 221, 0.4);
    }
</style>
""", unsafe_allow_html=True)

class NavigationSystem:
    def __init__(self, total_pages=1):
        self.total_pages = total_pages
    
    # ✅ NOVO MÉTODO INTERMEDIÁRIO
    def navigate_from_slider(self):
        """
        Lê o valor do slider a partir do session_state e navega para a página.
        """
        # A 'key' do slider é 'page_selector_optimized'
        new_page = st.session_state.page_selector_optimized
        self.navigate_to(new_page)
        
    def navigate_to(self, page_number):
        """Navega para uma página específica com verificação de limites"""
        if 1 <= page_number <= self.total_pages:
            st.session_state.pending_page = page_number
            st.session_state.page_change_confirmed = False
            return True
        return False

    def confirm_page_change(self):
        """Confirma a mudança de página"""
        if hasattr(st.session_state, 'pending_page'):
            st.session_state.current_page = st.session_state.pending_page
            # Limpa estados relacionados à página atual
            if hasattr(st.session_state, 'ia_analysis_result'):
                st.session_state.ia_analysis_result = None
            if hasattr(st.session_state, 'show_ia_analysis'):
                st.session_state.show_ia_analysis = False
    
    # ... (o restante da classe 'NavigationSystem' permanece igual) ...
    def next_page(self):
        current = st.session_state.get('current_page', 1)
        if current < self.total_pages:
            return self.navigate_to(current + 1)
        return False
    
    def prev_page(self):
        current = st.session_state.get('current_page', 1)
        if current > 1:
            return self.navigate_to(current - 1)
        return False
    
    def first_page(self):
        return self.navigate_to(1)
    
    def last_page(self):
        return self.navigate_to(self.total_pages)
        
    def update_total_pages(self, total_pages):
        self.total_pages = total_pages

class RenderController:
    def __init__(self):
        self._render_lock = False
        self._pending_operations = []
        self._last_render_time = 0
        self._render_interval = 0.5
        
    def should_render(self):
        current_time = time.time()
        if (current_time - self._last_render_time < self._render_interval or 
            self._render_lock):
            return False
        return True
        
    def acquire_lock(self):
        if not self._render_lock:
            self._render_lock = True
            return True
        return False
        
    def release_lock(self):
        self._render_lock = False
        self._last_render_time = time.time()
        
    def queue_operation(self, operation):
        self._pending_operations.append(operation)
        
    def execute_queued(self):
        for operation in self._pending_operations:
            try:
                operation()
            except Exception as e:
                print(f"Erro na operação enfileirada: {e}")
        self._pending_operations = []

class SearchEngine:
    """Motor de busca otimizado para livros grandes"""
    
    def __init__(self, segments, chapters):
        self.segments = segments
        self.chapters = chapters
        self._lazy_indexing = len(segments) > 1000  # Ativar indexação preguiçosa para livros grandes
        self.index_loaded = False
        
    def _ensure_index_loaded(self):
        """Garante que o índice está carregado (lazy loading)"""
        if not self.index_loaded:
            with st.spinner("📚 Carregando índice de busca..."):
                self._build_index()
                self.index_loaded = True
    
    def _build_index(self):
        """Constrói índice invertido para busca rápida"""
        self.word_index = {}
        self.phrase_index = {}
        self.chapter_index = {}
        
        # Indexar por capítulos
        for chapter in self.chapters:
            self.chapter_index[chapter['number']] = {
                'title': chapter['title'],
                'start_page': chapter['start_page'],
                'end_page': chapter['end_page']
            }
        
        # Indexar palavras e frases
        for i, segment in enumerate(self.segments):
            text = segment.get('text', '').lower()
            page_num = i + 1
            
            # Indexar palavras
            words = re.findall(r'\b\w+\b', text)
            for word in words:
                if word not in self.word_index:
                    self.word_index[word] = []
                self.word_index[word].append({
                    'page': page_num,
                    'positions': [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', text)]
                })
            
            # Indexar frases comuns (3-5 palavras)
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                sentence = sentence.strip()
                if 15 <= len(sentence) <= 200:  # Frases de tamanho razoável
                    if sentence not in self.phrase_index:
                        self.phrase_index[sentence] = []
                    self.phrase_index[sentence].append(page_num)
    
    def search_word(self, word, exact_match=False):
        """Busca com lazy loading"""
        if not self.index_loaded:
            self._ensure_index_loaded()
            
        results = []
        search_term = word.lower()
        
        if exact_match:
            if search_term in self.word_index:
                for entry in self.word_index[search_term]:
                    results.append({
                        'type': 'word',
                        'page': entry['page'],
                        'count': len(entry['positions']),
                        'excerpt': self._get_excerpt(entry['page'], search_term)
                    })
        else:
            # Busca parcial
            for term, entries in self.word_index.items():
                if search_term in term:
                    for entry in entries:
                        results.append({
                            'type': 'word',
                            'page': entry['page'],
                            'count': len(entry['positions']),
                            'excerpt': self._get_excerpt(entry['page'], term),
                            'matched_term': term
                        })
        
        return sorted(results, key=lambda x: x['count'], reverse=True)
    
    def _build_index_optimized(self):
        """Indexação otimizada para livros grandes"""
        self.word_index = {}
        self.phrase_index = {}
        self.chapter_index = {}
        
        # Indexar capítulos primeiro
        for chapter in self.chapters:
            self.chapter_index[chapter['number']] = {
                'title': chapter['title'],
                'start_page': chapter['start_page'],
                'end_page': chapter['end_page']
            }
        
        # Indexar em lotes para evitar sobrecarga de memória
        batch_size = 100  # Processar 100 páginas por vez
        total_pages = len(self.segments)
        
        for batch_start in range(0, total_pages, batch_size):
            batch_end = min(batch_start + batch_size, total_pages)
            
            for i in range(batch_start, batch_end):
                segment = self.segments[i]
                text = segment.get('text', '').lower()
                page_num = i + 1
                
                # Indexar palavras importantes (evitar palavras muito comuns)
                words = re.findall(r'\b\w+\b', text)
                word_counts = Counter(words)
                
                for word, count in word_counts.items():
                    # Ignorar palavras muito comuns ou muito curtas
                    if (len(word) > 3 and count > 0 and 
                        word not in self._get_stopwords()):
                        if word not in self.word_index:
                            self.word_index[word] = []
                        self.word_index[word].append({
                            'page': page_num,
                            'count': count
                        })
            
            # Limpar memória periodicamente
            if batch_start % 1000 == 0:
                import gc
                gc.collect()
    
    def _get_stopwords(self):
        """Lista de palavras comuns para ignorar na indexação"""
        return {
            'o', 'a', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'que', 'é', 'um', 'uma', 
            'os', 'as', 'se', 'por', 'uma', 'com', 'não', 'são', 'como', 'mas', 'foi', 'ao',
            'das', 'dos', 'nas', 'nos', 'pelo', 'pela', 'pelos', 'pelas', 'esse', 'essa',
            'isso', 'isto', 'aquele', 'aquela', 'aquilo', 'outro', 'outra', 'outros', 'outras',
            'qual', 'quais', 'quando', 'onde', 'quem', 'cujo', 'cuja', 'cujos', 'cujas',
            'que', 'quê', 'como', 'porque', 'porquê', 'porquê', 'porquê', 'porquê'
        }
    
    def search_phrase(self, phrase):
        """Busca por frase exata"""
        results = []
        search_phrase = phrase.lower().strip()
        
        # Busca direta no índice de frases
        if search_phrase in self.phrase_index:
            for page in self.phrase_index[search_phrase]:
                results.append({
                    'type': 'phrase',
                    'page': page,
                    'excerpt': self._get_excerpt(page, search_phrase, context_words=10)
                })
        
        # Busca aproximada para frases longas
        if not results and len(search_phrase.split()) > 3:
            words = search_phrase.split()
            first_word = words[0]
            
            if first_word in self.word_index:
                for entry in self.word_index[first_word]:
                    page_text = self.segments[entry['page'] - 1].get('text', '').lower()
                    if search_phrase in page_text:
                        results.append({
                            'type': 'phrase',
                            'page': entry['page'],
                            'excerpt': self._get_excerpt(entry['page'], search_phrase, context_words=15)
                        })
        
        return results
    
    def search_chapter(self, chapter_ref):
        """Busca por capítulo"""
        results = []
        
        # Tentar encontrar por número
        if isinstance(chapter_ref, int) or chapter_ref.isdigit():
            chapter_num = int(chapter_ref)
            if chapter_num in self.chapter_index:
                chapter = self.chapter_index[chapter_num]
                results.append({
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': chapter['title'],
                    'start_page': chapter['start_page'],
                    'end_page': chapter['end_page']
                })
        
        # Buscar por título
        for chapter_num, chapter_info in self.chapter_index.items():
            if (isinstance(chapter_ref, str) and 
                chapter_ref.lower() in chapter_info['title'].lower()):
                results.append({
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': chapter_info['title'],
                    'start_page': chapter_info['start_page'],
                    'end_page': chapter_info['end_page']
                })
        
        return results
    
    def search_verse(self, verse_ref):
        """Busca por versículo (padrão: capítulo:versículo)"""
        results = []
        
        # Padrão: 3:16 (capítulo 3, versículo 16)
        verse_pattern = r'(\d+)[:\.](\d+)'
        match = re.search(verse_pattern, verse_ref)
        
        if match:
            chapter_num = int(match.group(1))
            verse_num = int(match.group(2))
            
            # Encontrar capítulo
            if chapter_num in self.chapter_index:
                chapter = self.chapter_index[chapter_num]
                
                # Procurar versículo no capítulo
                verse_pattern = re.compile(rf'\b{verse_num}\b|\b{verse_num}[\.\:]', re.IGNORECASE)
                
                for page in range(chapter['start_page'], chapter['end_page'] + 1):
                    if page <= len(self.segments):
                        text = self.segments[page - 1].get('text', '')
                        if verse_pattern.search(text):
                            results.append({
                                'type': 'verse',
                                'chapter': chapter_num,
                                'verse': verse_num,
                                'page': page,
                                'excerpt': self._get_excerpt(page, str(verse_num), context_words=5)
                            })
        
        return results
    
    def _get_excerpt(self, page_num, search_term, context_words=5):
        """Obtém trecho do texto com o termo pesquisado"""
        if page_num > len(self.segments):
            return ""
        
        text = self.segments[page_num - 1].get('text', '')
        if not text:
            return ""
        
        # Encontrar posição do termo
        term_lower = search_term.lower()
        text_lower = text.lower()
        pos = text_lower.find(term_lower)
        
        if pos == -1:
            return text[:200] + "..." if len(text) > 200 else text
        
        # Obter contexto ao redor
        words = text.split()
        term_words = search_term.split()
        
        # Encontrar índice aproximado das palavras
        start_idx = max(0, len(text[:pos].split()) - context_words)
        end_idx = min(len(words), start_idx + len(term_words) + (context_words * 2))
        
        excerpt_words = words[start_idx:end_idx]
        excerpt = ' '.join(excerpt_words)
        
        # Destacar o termo encontrado
        highlighted = re.sub(
            re.escape(search_term), 
            f'<mark style="background-color: #ffeb3b; color: black; padding: 2px 4px; border-radius: 3px;">{search_term}</mark>',
            excerpt, 
            flags=re.IGNORECASE
        )
        
        return highlighted + "..." if end_idx < len(words) else highlighted
    
    def advanced_search(self, query, search_type="all", max_results=50):
        """Busca avançada com múltiplos critérios"""
        results = []
        
        if search_type in ["all", "word"]:
            results.extend(self.search_word(query, exact_match=(search_type == "word")))
        
        if search_type in ["all", "phrase"] and len(query.split()) > 1:
            results.extend(self.search_phrase(query))
        
        if search_type in ["all", "chapter"]:
            results.extend(self.search_chapter(query))
        
        if search_type in ["all", "verse"] and re.search(r'\d+[:\.]\d+', query):
            results.extend(self.search_verse(query))
        
        # Limitar resultados
        return results[:max_results]
    
class BookStateManager:
    def __init__(self):
        self.current_position = 0
        self.total_pages = 0
        self.loaded = False
        self.segments = []
        self._change_listeners = []
        
    def load_book(self, analysis_data):
        self.segments = analysis_data.get('segments', [])
        self.total_pages = len(self.segments)
        self.current_position = min(st.session_state.get('current_page', 1), self.total_pages)
        self.loaded = True
        return True
        
    def navigate_to(self, page_number):
        if 1 <= page_number <= self.total_pages:
            self.current_position = page_number
            self._notify_change()
            return True
        return False
        
    def _notify_change(self):
        for listener in self._change_listeners:
            try:
                listener(self.current_position)
            except Exception as e:
                print(f"Erro no listener: {e}")
                
    def get_current_segment(self):
        if 0 <= self.current_position - 1 < len(self.segments):
            return self.segments[self.current_position - 1]
        return {}
    
    def add_change_listener(self, listener):
        self._change_listeners.append(listener)

def safe_json_dump(data):
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        def escape_str(obj):
            if isinstance(obj, str):
                return (obj.replace("\\", "\\\\")
                         .replace('"', '\\"')
                         .replace('\n', '\\n')
                         .replace('\r', '\\r')
                         .replace('\t', '\\t'))
            elif isinstance(obj, dict):
                return {k: escape_str(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [escape_str(i) for i in obj]
            else:
                return obj
        return json.dumps(escape_str(data), ensure_ascii=False, indent=2)

def render_book_opener():
    st.title("📖 FLUX-ON Quantum Reader")
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(45, 45, 65, 0.8); border-radius: 20px; border: 3px solid #9d4edd;'>
        <h1 style='color: #e0aaff; margin-bottom: 2rem;'>Bem-vindo ao Leitor Quântico</h1>
        <p style='color: #c77dff; font-size: 1.2rem; margin-bottom: 3rem;'>
            Sistema avançado de análise e leitura multidimensional
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h3 style='color: #e0aaff;'>📚 Carregar Livro para Análise</h3>
            <p style='color: #c77dff;'>Selecione uma das opções abaixo para começar</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Carregar Análise Existente", use_container_width=True, key="load_existing"):
            st.session_state.book_loaded = True
        
        st.button("🆕 Analisar Novo Livro (Em Breve)", use_container_width=True, disabled=True)
        
        st.markdown("---")
        st.info("""
        **💡 Dica:** Use a opção 'Carregar Análise Existente' para visualizar 
        relatórios já processados pelo sistema FLUX-ON.
        """)

class QuantumBookReader:
    def __init__(self, analysis_data=None):
        self.analysis_data = analysis_data or {}
        self.segments = self.analysis_data.get('segments', [])
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
            
        # CORREÇÃO: Atualizar total_pages do nav_system
        self.nav_system = NavigationSystem(len(self.segments))
        self.state_manager = BookStateManager()
        self.render_controller = RenderController()
        
        self.state_manager.add_change_listener(self._on_page_change)
        
        if analysis_data:
            self.state_manager.load_book(analysis_data)
            
        self.ia_prompts = self._initialize_prompts()
        self._processed_text_cache = {}
        
        self.chapters = self._extract_chapters_advanced()
        
        self.search_engine = SearchEngine(self.segments, self.chapters)
        self.search_results = []
        self.current_search_query = ""
        
        self.api_config = {
            'configured': False,
            'api_key': '',
            'api_url': 'https://api.deepseek.com/v1/chat/completions',
            'model': 'deepseek-chat'
        }
        
        self.extended_themes = {
            'política': {
                'keywords': ['governo', 'presidente', 'eleições', 'democracia', 'ditadura', 'político', 
                        'partido', 'estado', 'lei', 'justiça', 'poder', 'corrupção', 'voto', 'parlamento',
                        'legislativo', 'executivo', 'ministro', 'prefeito', 'vereador', 'senador',
                        'deputado', 'política', 'ideologia', 'partidário', 'coalizão', 'oposição'],
                'weight': 0.7
            },
            'religião': {
                'keywords': ['deus', 'fé', 'igreja', 'bíblia', 'oração', 'espiritual', 'divino', 'sagrado',
                        'profeta', 'religioso', 'crença', 'culto', 'ritual', 'teologia', 'pecado',
                        'bispo', 'padre', 'pastor', 'templo', 'sinagoga', 'mesquita', 'deus',
                        'jesus', 'cristo', 'allah', 'budismo', 'hinduísmo', 'espiritualidade'],
                'weight': 0.6
            },
            'sexo': {
                'keywords': ['sexual', 'gênero', 'masculino', 'feminino', 'relação', 'corpo', 'desejo',
                        'intimidade', 'orientação', 'identidade', 'atração', 'reprodução', 'prazer',
                        'sensual', 'erótico', 'afetividade', 'casamento', 'namoro', 'paixão', 'amor',
                        'heterossexual', 'homossexual', 'bissexual', 'transgênero', 'libido'],
                'weight': 0.5
            },
            'cultura': {
                'keywords': ['arte', 'música', 'literatura', 'tradição', 'costumes', 'sociedade', 'valores',
                        'identidade', 'folclore', 'herança', 'expressão', 'cultural', 'patrimônio',
                        'dança', 'teatro', 'cinema', 'pintura', 'escultura', 'fotografia', 'arquitetura',
                        'festival', 'celebração', 'ritual', 'mitologia', 'história', 'ancestral'],
                'weight': 0.8
            }
        }
        
        self._initialize_session_state()
        self.book_analysis = self.analysis_data.get('book_analysis', {})
    
    def _initialize_session_state(self):
        # CORREÇÃO: Garantir que current_page está inicializado
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
            
        if 'user_highlights' not in st.session_state:
            st.session_state.user_highlights = {}
            
        if 'user_notes' not in st.session_state:
            st.session_state.user_notes = {}
            
        if 'show_ia_analysis' not in st.session_state:
            st.session_state.show_ia_analysis = False
            
        if 'selected_text_for_analysis' not in st.session_state:
            st.session_state.selected_text_for_analysis = ""
            
        if 'ia_analysis_result' not in st.session_state:
            st.session_state.ia_analysis_result = None
            
        if 'ia_prompt_used' not in st.session_state:
            st.session_state.ia_prompt_used = None
            
        if 'book_loaded' not in st.session_state:
            st.session_state.book_loaded = False
            
        if 'book_cover_shown' not in st.session_state:
            st.session_state.book_cover_shown = False
            
        if 'api_configured' not in st.session_state:
            st.session_state.api_configured = False
            
        if 'deepseek_response' not in st.session_state:
            st.session_state.deepseek_response = None
            
        if 'local_analysis' not in st.session_state:
            st.session_state.local_analysis = None
            
        if 'copied_prompt' not in st.session_state:
            st.session_state.copied_prompt = None
        
        if 'page_change_confirmed' not in st.session_state:
            st.session_state.page_change_confirmed = False
    
    def _on_page_change(self, new_page):
        st.session_state.current_page = new_page
        if 'ia_analysis_result' in st.session_state:
            st.session_state.ia_analysis_result = None
    
    def load_analysis_data(self, analysis_data):
        self.analysis_data = analysis_data
        self.segments = analysis_data.get('segments', [])
        self.state_manager.load_book(analysis_data)
        self.nav_system.update_total_pages(len(self.segments))
        self.chapters = self._extract_chapters_advanced()
        st.session_state.book_loaded = True
        
    def render_advanced_search_sidebar(self):
        """Sidebar com busca avançada e filtros"""
        with st.sidebar:
            st.markdown("---")
            st.header("🔍 Busca Avançada")
            
            # Campo de busca principal
            search_query = st.text_input(
                "O que você está procurando?",
                placeholder="Digite palavra, frase, capítulo ou versículo...",
                key="main_search_input"
            )
            
            # Filtros avançados
            with st.expander("⚙️ Filtros Avançados", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    search_type = st.selectbox(
                        "Tipo de busca:",
                        ["Todos", "Palavras", "Frases", "Capítulos", "Versículos"],
                        key="search_type_filter"
                    )
                    
                    case_sensitive = st.checkbox("Diferenciar maiúsc/minúsc", False)
                
                with col2:
                    min_word_length = st.slider("Tamanho mínimo palavra:", 3, 10, 4)
                    max_results = st.slider("Máx. resultados:", 10, 200, 50)
            
            # Botões de ação
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔎 Buscar", use_container_width=True) and search_query:
                    self.perform_search(search_query, search_type, case_sensitive, max_results)
            
            with col2:
                if st.button("🧹 Limpar", use_container_width=True):
                    self.search_results = []
                    self.current_search_query = ""
            
            # Resultados rápidos na sidebar
            if self.search_results:
                st.markdown("---")
                st.subheader("📋 Resultados Encontrados")
                
                for i, result in enumerate(self.search_results[:3]):
                    emoji = "📖" if result['type'] == 'chapter' else "📜" if result['type'] == 'verse' else "📄"
                    st.info(f"{emoji} {self._format_search_result(result)}")
                    
                    if st.button("Ir →", key=f"sidebar_goto_{i}", use_container_width=True):
                        st.session_state.current_page = result['page']
                        st.rerun()
                
                if len(self.search_results) > 3:
                    st.info(f"📊 ... e mais {len(self.search_results) - 3} resultados")
                    
                    if st.button("Ver todos os resultados", use_container_width=True):
                        st.session_state.current_menu = "🔍 Resultados Busca"
                        st.rerun()

    def _format_search_result(self, result):
        """Formata resultado para exibição compacta"""
        if result['type'] == 'chapter':
            return f"Capítulo {result['number']}: {result['title']}"
        elif result['type'] == 'verse':
            return f"Versículo {result['chapter']}:{result['verse']}"
        elif result['type'] == 'word':
            return f"Palavra: {result.get('matched_term', '')} ({result['count']}x)"
        elif result['type'] == 'phrase':
            return "Frase encontrada"
        return "Resultado"
    
    @st.cache_data(show_spinner=False, max_entries=100)
    def _process_text_highlights_cached(_self, text, keywords, entities, page_highlights):
        highlighted_text = text
        
        for highlight_id, highlight_data in page_highlights.items():
            highlighted_text = highlighted_text.replace(
                highlight_data['text'],
                f'<span class="user-highlight" title="Destacado pelo usuário">{highlight_data["text"]}</span>'
            )
        
        for entity, label in entities[:10]:
            if entity not in highlighted_text:
                highlighted_text = re.sub(
                    re.escape(entity),
                    f'<span class="highlight-important" title="{label}">{entity}</span>',
                    highlighted_text,
                    flags=re.IGNORECASE
                )
        
        for keyword in keywords[:15]:
            if keyword not in highlighted_text:
                highlighted_text = re.sub(
                    f'\\b{re.escape(keyword)}\\b',
                    f'<span class="highlight">{keyword}</span>',
                    highlighted_text,
                    flags=re.IGNORECASE
                )
        
        return highlighted_text
    
    def _generate_text_analysis_prompt(self, prompt_type, text, segment=None):
        """Gera prompt contextualizado baseado no tipo de análise"""
        book_name = self.analysis_data.get('book_name', 'este livro')
        current_page = st.session_state.current_page
        current_chapter = self._get_current_chapter()
        
        chapter_info = f"Capítulo {current_chapter['number']}: {current_chapter['title']}" if current_chapter else "Contexto geral"
        
        prompts = {
            'page_summary': f"""Gere um resumo detalhado da página {current_page} do livro "{book_name}".
    Contexto: {chapter_info}
    Texto: {text[:2000]}
    Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro.""",
            
            'analysis': f"""Analise profundamente este texto considerando:
    1. Contexto histórico e significado filosófico
    2. Metáforas, simbolismos e linguagem figurada  
    3. Relações com temas maiores da obra
    4. Implicações científicas, filosóficas ou sociais
    5. Conexões com outros conceitos apresentados no livro

    Contexto: {chapter_info}
    Livro: {book_name}
    Texto para análise: {text[:2000]}""",
            
            'explain_concepts': f"""Explique os conceitos complexos presentes no texto:
    Contexto: {chapter_info}
    Livro: {book_name}
    Texto: {text[:2000]}
    Forneça definições claras, exemplos práticos e relação com o contexto do livro.""",
            
            'chapter_context': f"""Considerando que este texto faz parte do {chapter_info} do livro "{book_name}",
    analise como este trecho se relaciona com:
    1. O contexto geral do capítulo
    2. A estrutura narrativa do livro  
    3. Os temas principais da obra
    4. O desenvolvimento de ideias ao longo do livro

    Trecho para análise: {text[:2000]}"""
        }
        
        return prompts.get(prompt_type, f"Analise o seguinte texto: {text[:2000]}")
    
    def _format_text_for_display(self, text):
        if not text:
            return text
            
        text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
        text = re.sub(r'([,:;])([A-Za-z])', r'\1 \2', text)
        
        chapter_patterns = [
            r'(?i)^(capítulo|chapter|cap\.)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)$',
            r'^(CAPÍTULO|CHAPTER)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)$',
            r'^(\d+|[IVXLCDM]+)[\s.-]+\s*(.*)$'
        ]
        
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line_formatted = line
            for pattern in chapter_patterns:
                match = re.match(pattern, line.strip())
                if match:
                    groups = match.groups()
                    if len(groups) >= 3 and groups[2]:
                        line_formatted = f'<h3 class="chapter-title">{groups[0]} {groups[1]}: {groups[2]}</h3>'
                    elif len(groups) >= 2:
                        line_formatted = f'<h3 class="chapter-title">{groups[0]} {groups[1]}</h3>'
                    break
            formatted_lines.append(line_formatted)
        
        text = '\n'.join(formatted_lines)
        
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            formatted_paragraphs = []
            for paragraph in paragraphs:
                if paragraph.strip():
                    if len(paragraph.strip()) < 100 and not re.search(r'[.!?]$', paragraph):
                        formatted_paragraphs.append(f'<p class="short-paragraph">{paragraph.strip()}</p>')
                    else:
                        paragraph_text = paragraph.strip()
                        formatted_paragraphs.append(f'<p>{paragraph_text}</p>')
            text = '\n\n'.join(formatted_paragraphs)
        else:
            text = f'<p>{text}</p>'
        
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def render_search_interface(self):
        """Renderiza a interface de busca avançada"""
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Busca Avançada")
        
        # Campo de busca
        search_query = st.sidebar.text_input(
            "Digite sua busca:",
            placeholder="Palavra, frase, capítulo ou versículo...",
            key="search_input"
        )
        
        # Tipo de busca
        search_type = st.sidebar.selectbox(
            "Tipo de busca:",
            ["Todos", "Palavras", "Frases", "Capítulos", "Versículos"],
            key="search_type"
        )
        
        # Botão de busca
        if st.sidebar.button("🔎 Buscar", use_container_width=True) and search_query:
            with st.spinner("Buscando..."):
                search_type_map = {
                    "Todos": "all",
                    "Palavras": "word", 
                    "Frases": "phrase",
                    "Capítulos": "chapter",
                    "Versículos": "verse"
                }
                
                self.current_search_query = search_query
                self.search_results = self.search_engine.advanced_search(
                    search_query, 
                    search_type_map[search_type]
                )
        
        # Exibir resultados se houver
        if self.search_results:
            st.sidebar.markdown(f"**📊 {len(self.search_results)} resultado(s) encontrado(s)**")
            
            for i, result in enumerate(self.search_results[:5]):  # Mostrar primeiros 5
                result_type = result['type']
                if result_type == 'chapter':
                    st.sidebar.info(f"📖 Capítulo {result['number']}: {result['title']} (páginas {result['start_page']}-{result['end_page']})")
                elif result_type == 'verse':
                    st.sidebar.info(f"📜 {result['chapter']}:{result['verse']} - Página {result['page']}")
                else:
                    st.sidebar.info(f"📄 Página {result['page']} - {result.get('count', 1)} ocorrência(s)")
                
                if st.sidebar.button("Ir para", key=f"goto_{i}", use_container_width=True):
                    st.session_state.current_page = result['page']
                    st.rerun()
            
            if len(self.search_results) > 5:
                st.sidebar.info(f"📋 ... e mais {len(self.search_results) - 5} resultados")
    
    def render_search_results_page(self):
        """Página dedicada aos resultados de busca"""
        if not self.search_results:
            return
        
        st.title(f"🔍 Resultados da busca: '{self.current_search_query}'")
        st.markdown(f"**📊 {len(self.search_results)} resultado(s) encontrado(s)**")
        
        # Agrupar resultados por página
        results_by_page = {}
        for result in self.search_results:
            page = result['page']
            if page not in results_by_page:
                results_by_page[page] = []
            results_by_page[page].append(result)
        
        # Exibir resultados organizados
        for page, page_results in sorted(results_by_page.items()):
            with st.expander(f"📄 Página {page} - {len(page_results)} resultado(s)", expanded=False):
                for result in page_results:
                    if result['type'] == 'word':
                        st.markdown(f"**Palavra:** {result.get('matched_term', self.current_search_query)}")
                        st.markdown(f"**Ocorrências:** {result['count']}")
                    elif result['type'] == 'phrase':
                        st.markdown("**Frase encontrada:**")
                    elif result['type'] == 'verse':
                        st.markdown(f"**Versículo:** {result['chapter']}:{result['verse']}")
                    
                    # Exibir trecho
                    if 'excerpt' in result:
                        st.markdown(f"**Trecho:** {result['excerpt']}", unsafe_allow_html=True)
                    
                    # Botão para ir para a página
                    if st.button("Ir para esta página", key=f"result_goto_{page}_{result['type']}"):
                        st.session_state.current_page = page
                        st.rerun()
                    
                    st.markdown("---")

    def _render_interactive_text(self, segment):
        raw_text = segment.get('text', '')
        
        if not raw_text:
            st.warning("📝 Conteúdo não disponível para esta página")
            return
        
        formatted_text = self._format_text_for_display(raw_text)
        
        analysis = segment.get('analysis', {})
        keywords = analysis.get('keywords', [])[:8]
        entities = analysis.get('entities', [])[:5]
        
        page_highlights = {}
        if (st.session_state.current_page in st.session_state.user_highlights and 
            st.session_state.user_highlights[st.session_state.current_page]):
            page_highlights = st.session_state.user_highlights[st.session_state.current_page]
        
        highlighted_text = self._process_text_highlights_cached(
            formatted_text, keywords, entities, page_highlights
        )
        
        st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;'>
            <h2>📖 Conteúdo da Página</h2>
            <div style='color: #c77dff; font-size: 1rem;'>
                🎨 <strong>Destacados:</strong> 
                <span style='background: #9d4edd40; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Palavras-chave</span>
                <span style='background: #ff6b6b40; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Entidades</span>
                <span style='background: #4cc9f040; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Seleção</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='text-container focus-effect'>
            {highlighted_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🔍 Ferramentas de Análise de Texto")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_text = st.text_input(
                "Selecionar texto para análise:",
                placeholder="Digite ou cole o texto que deseja analisar",
                key=f"text_select_{st.session_state.current_page}"
            )
        
        with col2:
            st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
            if st.button("🔍 Analisar Texto", use_container_width=True) and selected_text:
                if st.session_state.current_page not in st.session_state.user_highlights:
                    st.session_state.user_highlights[st.session_state.current_page] = {}
                
                highlight_id = f"highlight_{len(st.session_state.user_highlights[st.session_state.current_page]) + 1}"
                st.session_state.user_highlights[st.session_state.current_page][highlight_id] = {
                    'text': selected_text,
                    'page': st.session_state.current_page
                }
                
                st.session_state.selected_text_for_analysis = selected_text
                st.session_state.show_ia_analysis = True
                
                st.success("Texto destacado para análise!")
        
        if keywords or entities or page_highlights:
            st.markdown("---")
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                if keywords:
                    st.caption(f"🔑 **Palavras-chave:** {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
            
            with info_col2:
                if entities:
                    entity_list = [f"{e[0]} ({e[1]})" for e in entities[:3]]
                    st.caption(f"🏷️ **Entidades:** {', '.join(entity_list)}{'...' if len(entities) > 3 else ''}")
            
            with info_col3:
                if page_highlights:
                    highlight_count = len(page_highlights)
                    st.caption(f"⭐ **Seleções do usuário:** {highlight_count} texto(s) destacado(s)")
    
    def _initialize_prompts(self):
        return {
            'summary': """Analise o seguinte texto e forneça um resumo conciso em português. 
Destaque os pontos principais, conceitos-chave e a mensagem central:""",
            
            'analysis': """Analise profundamente este texto considerando:
1. Contexto histórico e significado filosófico
2. Metáforas, simbolismos e linguagem figurada
3. Relações com temas maiores da obra
4. Implicações científicas, filosóficas ou sociais
5. Conexões com outros conceitos apresentados no livro

Texto para análise:""",
            
            'explain_concepts': """Explique os seguintes conceitos presentes no texto: {concepts}
Forneça definições claras, exemplos práticos e relação con o contexto do livro:""",
            
            'chapter_context': """Considerando que este texto faz parte do capítulo "{chapter}" do livro "{book_name}",
analise como este trecho se relaciona con:
1. O contexto geral do capítulo
2. A estrutura narrativa do livro
3. Os temas principais da obra
4. O desenvolvimento de ideias ao longo do livro

Trecho para análise:""",
            
            'page_summary': """Gere um resumo detalhado da página {page} do livro "{book_name}". 
Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro:""",
            
            'highlight_analysis': """Analise o seguinte texto destacado pelo usuário: "{highlighted_text}"
Contexto do trecho: {context}
Forneça uma análise aprofundada do significado, importância e relações com o conteúdo do livro:"""
        }
    
    def _extract_chapters_advanced(self):
        chapters = []
        current_chapter = None
        chapter_patterns = [
            r'(capítulo|chapter|cap\.)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)',
            r'^(CAPÍTULO|CHAPTER)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)',
            r'^(\d+|[IVXLCDM]+)[\s.-]*(.*)',
            r'^.*\b(capítulo|chapter)\b.*$'
        ]
        
        for i, segment in enumerate(self.segments):
            text = segment.get('text', '').strip()
            
            if len(text) > 300:
                if current_chapter:
                    current_chapter['end_page'] = i
                continue
                
            chapter_detected = False
            chapter_title = ""
            chapter_number = ""
            
            for pattern in chapter_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    chapter_detected = True
                    groups = match.groups()
                    
                    if len(groups) >= 2:
                        chapter_number = groups[1] if groups[1] else str(len(chapters) + 1)
                        chapter_title = groups[2] if len(groups) > 2 and groups[2] else f"Capítulo {chapter_number}"
                    else:
                        chapter_number = str(len(chapters) + 1)
                        chapter_title = text
                    
                    break
            
            is_toc = any(word in text.lower() for word in ['sumário', 'índice', 'conteúdo', 'contents'])
            
            if chapter_detected and not is_toc:
                if current_chapter:
                    current_chapter['end_page'] = i
                
                current_chapter = {
                    'number': chapter_number,
                    'title': chapter_title,
                    'start_page': i + 1,
                    'end_page': len(self.segments),
                    'segments': [i + 1]
                }
                chapters.append(current_chapter)
            elif current_chapter and not is_toc:
                current_chapter['segments'].append(i + 1)
        
        return chapters
    
    def render_advanced_sidebar(self):
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(157, 78, 221, 0.1); border-radius: 15px;'>
                <h1 style='font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #e0aaff, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📖 FLUX-ON READER</h1>
                <p style='color: #c77dff; margin: 0; font-size: 1.1rem;'>Leitura Quântica Multidimensional</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.header("🔢 Navegação Rápida")
            nav_col1, nav_col2, nav_col3 = st.columns(3)
            
            with nav_col1:
                if st.button("⏮️ Primeira", use_container_width=True, help="Ir para a primeira página"):
                    self.nav_system.first_page()
            
            with nav_col2:
                if st.button("◀️ Anterior", use_container_width=True, help="Página anterior"):
                    self.nav_system.prev_page()
            
            with nav_col3:
                if st.button("Próxima ▶️", use_container_width=True, help="Próxima página"):
                    self.nav_system.next_page()
            
            # ✅ BOTÃO DE CONFIRMAÇÃO (só aparece quando há mudança pendente)
            if hasattr(st.session_state, 'pending_page') and st.session_state.pending_page != st.session_state.get('current_page', 1):
                st.markdown("---")
                if st.button("✅ **CONFIRMAR MUDANÇA DE PÁGINA**", 
                            use_container_width=True,
                            type="primary",
                            help="Clique para carregar a página selecionada"):
                    self.nav_system.confirm_page_change()
                    st.rerun()  # Força a atualização após confirmação
                
                st.info(f"📖 Página {st.session_state.pending_page} selecionada. Confirme para carregar.")
            
            st.header("🎯 Navegação por Página")

            # ✅ CORREÇÃO: O select_slider já funciona bem com o session_state
            selected_page = st.select_slider(
                "Selecionar página:",
                options=list(range(1, len(self.segments) + 1)),
                value=st.session_state.current_page,
                key="page_selector_optimized",
                on_change=lambda: setattr(st.session_state, 'pending_page', st.session_state.page_selector_optimized)
            )
            
            metrics_data = [
                ("📄 Total de páginas", len(self.segments)),
                ("📝 Palavras totais", self.book_analysis.get('total_words', 0)),
                ("🎯 Dificuldade média", f"{self.book_analysis.get('avg_difficulty', 0):.1f}/100"),
                ("📈 Variação de dificuldade", f"{self.book_analysis.get('max_difficulty', 0) - self.book_analysis.get('min_difficulty', 0):.1f}")
            ]
            
            for metric, value in metrics_data:
                st.metric(metric, value)
            
            st.header("🎯 Temas Principais")
            # CORREÇÃO: Usar self.book_analysis
            theme_dist = self.book_analysis.get('theme_distribution', {})
            
            if theme_dist:
                all_text = " ".join([segment.get('text', '') for segment in self.segments])
                extended_themes = self._analyze_extended_themes(all_text)
                
                combined_themes = {**theme_dist, **extended_themes}
                
                for theme, score in sorted(combined_themes.items(), key=lambda x: x[1], reverse=True)[:8]:
                    st.progress(score/100, f"{theme}: {score:.1f}%")
            else:
                st.info("Análise de temas em andamento...")
                
            st.markdown("---")
            if st.button("🏠 Voltar à Tela Inicial", use_container_width=True, key="back_to_main"):
                st.session_state.book_loaded = False
    
    def _get_current_chapter(self):
        current_page = st.session_state.current_page
        for chapter in self.chapters:
            if current_page >= chapter['start_page'] and current_page <= chapter['end_page']:
                return chapter
        return None
    
    def _render_visual_analysis(self, segment):
        st.markdown("---")
        st.header("📊 Análise Visual da Página")
        
        col1, col2 = st.columns(2)
        
        with col1:
            metrics = segment.get('complexity_metrics', {})
            if metrics:
                metrics_names = ['Palavras', 'Sentenças', 'Pal./Sentença', 'Tam. Médio']
                metrics_values = [
                    metrics.get('word_count', 0),
                    metrics.get('sentence_count', 0),
                    metrics.get('avg_sentence_length', 0),
                    metrics.get('avg_word_length', 0)
                ]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=metrics_values,
                    theta=metrics_names,
                    fill='toself',
                    name='Métricas',
                    line_color='#e0aaff',
                    fillcolor='rgba(224, 170, 255, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(30, 30, 46, 0.3)',
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(metrics_values) * 1.2]
                        ),
                    ),
                    showlegend=False,
                    title="📈 Métricas de Complexidade (Radar)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff', size=12),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            themes = segment.get('themes', {})
            if themes and len(themes) > 0:
                text_analysis = self._analyze_text_patterns(segment.get('text', ''))
                extended_themes = text_analysis.get('extended_themes', {})
                
                all_themes = {**themes, **extended_themes}
                themes_df = pd.DataFrame({
                    'Tema': list(all_themes.keys()),
                    'Intensidade': list(all_themes.values())
                }).sort_values('Intensidade', ascending=False).head(8)
                
                fig = px.pie(themes_df, values='Intensidade', names='Tema', 
                            title="🎯 Distribuição de Temas (Incluindo Novos)",
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Set3)
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    showlegend=True,
                    height=400,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("🔍 Análise de temas em andamento...")
        
        st.markdown("---")
        st.subheader("🌍 Análise de Temas Sociais e Culturais")
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        extended_themes = text_analysis.get('extended_themes', {})
        
        if extended_themes:
            theme_cols = st.columns(4)
            
            for i, (theme, score) in enumerate(extended_themes.items()):
                if score > 5:
                    with theme_cols[i % 4]:
                        icons = {
                            'política': '🏛️',
                            'religião': '🙏',
                            'sexo': '❤️',
                            'cultura': '🎭'
                        }
                        
                        st.metric(
                            label=f"{icons.get(theme, '📊')} {theme.capitalize()}",
                            value=f"{score:.1f}%",
                            help=f"Intensidade do tema {theme} nesta página"
                        )
            
            if any(score > 5 for score in extended_themes.values()):
                extended_df = pd.DataFrame({
                    'Tema': list(extended_themes.keys()),
                    'Intensidade': list(extended_themes.values())
                }).sort_values('Intensidade', ascending=False)
                
                fig = px.bar(extended_df, x='Tema', y='Intensidade',
                            title="📊 Intensidade dos Temas Sociais",
                            color='Intensidade',
                            color_continuous_scale='viridis')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🤔 Nenhum tema social significativo detectado nesta página.")
        
        sentiment_score = max(0, min(100, segment.get('difficulty', 0) * 0.8))
        sentiment_label = "Positivo" if sentiment_score > 60 else "Neutro" if sentiment_score > 40 else "Desafiador"
        sentiment_icon = "😊" if sentiment_score > 60 else "😐" if sentiment_score > 40 else "😔"
        
        st.markdown("---")
        sentiment_col1, sentiment_col2, sentiment_col3 = st.columns([1, 2, 1])
        
        with sentiment_col2:
            html = f"""
            <div style='text-align: center; padding: 1.5rem; background: rgba(45, 45, 65, 0.7); border-radius: 15px; border-left: 5px solid #7b2cbf;'>
                <h3 style='color: #e0aaff; margin-bottom: 1rem;'>🎭 Tom Emocional da Página</h3>
                <div style='font-size: 2.5rem; font-weight: bold; color: #e0aaff; margin: 0.5rem 0;'>{sentiment_icon} {sentiment_label}</div>
                <div style='margin-top: 1.5rem; position: relative;'>
                    <div style='background: rgba(255,255,255,0.1); height: 25px; border-radius: 12px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #f44336, #ff9800, #4caf50); 
                                height: 100%; width: {sentiment_score:.1f}%; border-radius: 12px; 
                                position: relative;'>
                            <div style='position: absolute; right: 5px; top: 50%; transform: translateY(-50%); 
                                    color: white; font-weight: bold; font-size: 12px;'>
                                {sentiment_score:.1f}%
                            </div>
                        </div>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-top: 0.5rem; color: #c77dff; font-size: 0.9rem;'>
                        <span>Desafiador</span>
                        <span>Neutro</span>
                        <span>Positivo</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    
    def _analyze_extended_themes(self, text):
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        total_words = len(words)
        
        if total_words == 0:
            return {theme: 0 for theme in self.extended_themes.keys()}
        
        theme_scores = {}
        
        for theme, theme_data in self.extended_themes.items():
            score = 0
            keyword_count = 0
            
            for keyword in theme_data['keywords']:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                count = len(re.findall(pattern, text_lower))
                
                if count > 0:
                    word_weight = theme_data['weight']
                    
                    common_word_penalty = 1.0
                    if keyword in ['poder', 'estado', 'lei', 'corpo', 'valor']:
                        common_word_penalty = 0.6
                    
                    score += (count * word_weight * common_word_penalty)
                    keyword_count += count
            
            density = (keyword_count / total_words) * 1000
            
            if density > 0:
                normalized_score = min(100, 20 * math.log1p(density))
            else:
                normalized_score = 0
            
            diversity_bonus = 1.0
            if keyword_count > 5:
                diversity_bonus = 1.2
            
            theme_scores[theme] = min(100, normalized_score * diversity_bonus)
        
        return theme_scores

    def _analyze_text_patterns(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        stopwords = {'o', 'a', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'que', 'é', 'um', 'uma', 'os', 'as'}
        relevant_words = {word: count for word, count in word_freq.items() 
                         if word not in stopwords and len(word) > 3 and count > 1}
        
        scientific_terms = {'energia', 'quantum', 'consciência', 'evolução', 'comportamento', 
                           'física', 'mente', 'universo', 'realidade', 'matéria', 'filosofia'}
        
        found_terms = {term: word_freq.get(term, 0) for term in scientific_terms 
                      if term in word_freq}
        
        extended_themes = self._analyze_extended_themes(text)
        
        return {
            'frequent_words': dict(sorted(relevant_words.items(), 
                                        key=lambda x: x[1], reverse=True)[:15]),
            'scientific_terms': found_terms,
            'extended_themes': extended_themes,
            'total_words': len(words),
            'unique_words': len(set(words))
        }

    def _render_api_configuration(self):
        st.markdown("---")
        st.header("🔧 Configuração da API DeepSeek")
        
        with st.expander("⚙️ Configurar Conexão com IA", expanded=False):
            st.info("""
            **Para usar análises com IA em tempo real:**
            1. Obtenha uma chave API em: https://platform.deepseek.com/
            2. Cole sua chave API abaixo
            3. Salve as configurações
            """)
            
            api_key = st.text_input(
                "🔑 Chave API DeepSeek:",
                type="password",
                placeholder="sk-...",
                help="Insira sua chave API do DeepSeek"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Salvar Configurações", use_container_width=True):
                    if api_key:
                        self.api_config['api_key'] = api_key
                        self.api_config['configured'] = True
                        st.session_state.api_configured = True
                        st.success("✅ Configurações salvas com sucesso!")
                    else:
                        st.error("❌ Por favor, insira uma chave API válida")
            
            with col2:
                if st.button("🧪 Testar Conexão", use_container_width=True):
                    if api_key:
                        with st.spinner("Testando conexão com DeepSeek..."):
                            success = self._test_api_connection(api_key)
                            if success:
                                st.success("✅ Conexão com API estabelecida com sucesso!")
                            else:
                                st.error("❌ Falha na conexão. Verifique sua chave API.")
                    else:
                        st.warning("⚠️ Insira uma chave API primeiro")
            
            if self.api_config['configured']:
                st.markdown("---")
                st.success("✅ API Configurada - Análises em tempo real disponíveis")
                if st.button("🗑️ Remover Configuração", type="secondary", use_container_width=True):
                    self.api_config['configured'] = False
                    self.api_config['api_key'] = ''
                    st.session_state.api_configured = False
    
    def _test_api_connection(self, api_key: str) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Teste de conexão. Responda com 'OK'."}],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(
                self.api_config['api_url'],
                headers=headers,
                json=payload,
                timeout=15
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def _call_deepseek_api(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            if not self.api_config['configured'] or not self.api_config['api_key']:
                st.warning("🔧 API não configurada. Usando análise inteligente local.")
                return self._fallback_analysis(prompt)
            
            headers = {
                "Authorization": f"Bearer {self.api_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é um especialista em análise literária e científica. Forneça análises profundas e insights valiosos baseados no texto fornecido. Seja conciso, claro e focado nos aspectos mais relevantes. Responda em português."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            api_url = "https://api.deepseek.com/v1/chat/completions"
            
            with st.spinner("🔗 Conectando com DeepSeek AI..."):
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                st.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout na conexão com a API. Verifique sua internet.")
            return self._fallback_analysis(prompt)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                st.error("🔐 Erro de autenticação. Verifique sua chave API.")
            elif e.response.status_code == 429:
                st.warning("🚦 Limite de requisições excedido. Usando análise local.")
            else:
                st.error(f"❌ Erro HTTP {e.response.status_code}: {e.response.text}")
            return self._fallback_analysis(prompt)
            
        except Exception as e:
            st.error(f"⚠️ Erro na chamada da API: {str(e)}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        return f"""
        **📊 Análise Local - FLUX-ON Reader**

        🔧 **Status:** API DeepSeek não disponível no momento

        💡 **Para ativar análises completas:**
        1. Configure sua chave API em: https://platform.deepseek.com/
        2. Adicione créditos à sua conta
        3. Sua chave atual: `{self.api_config.get('api_key', 'Não configurada')}`

        **📋 Prompt que seria enviado:**
        {prompt}
        """

    def _render_analysis_tools(self, segment):
        st.markdown("---")
        
        # MOVER AS ABAS PARA A SIDEBAR - ESTRUTURA REORGANIZADA
        with st.sidebar:
            st.markdown("---")
            st.header("🧰 Ferramentas de Análise")
            
            # Abas verticais na sidebar
            selected_tool = st.radio(
                "Selecione a ferramenta:",
                ["🤖 Análise IA", "🔍 Insights", "📝 Anotações", "⭐ Textos Destacados"],
                key="analysis_tools_sidebar"
            )
        
        # Container principal para o conteúdo das ferramentas
        analysis_container = st.container()
        
        with analysis_container:
            if selected_tool == "🤖 Análise IA":
                self._render_ia_analysis_tab(segment)
                
            elif selected_tool == "🔍 Insights":
                self._render_insights_tab(segment)
                
            elif selected_tool == "📝 Anotações":
                self._render_notes_tab()
                
            elif selected_tool == "⭐ Textos Destacados":
                self._render_highlights_tab()

    def _render_ia_analysis_tab(self, segment):
        st.subheader("🤖 Análise com Inteligência Artificial")
        
        if self.api_config['configured']:
            st.success("✅ API Configurada - Análises em tempo real")
        else:
            st.warning("🔧 API não configurada - Usando análise local")
            st.info("💡 Configure a API DeepSeek para análises mais precisas")
        
        analysis_options = {
            "Resumo da Página": "page_summary",
            "Análise Profunda": "analysis",
            "Explicar Conceitos": "explain_concepts",
            "Contexto do Capítulo": "chapter_context"
        }
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analysis_type = st.selectbox(
                "Tipo de análise:",
                list(analysis_options.keys()),
                help="Selecione o tipo de análise que deseja realizar"
            )
        
        with col2:
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            if st.button("🚀 Gerar Análise", use_container_width=True):
                with st.spinner("🤖 Processando análise..."):
                    prompt_type = analysis_options[analysis_type]
                    # CORREÇÃO: Usar o método correto para gerar prompt
                    prompt = self._generate_text_analysis_prompt(prompt_type, segment.get('text', '')[:3000], segment)
                    
                    st.session_state.ia_prompt = prompt
                    analysis_result = self._call_deepseek_api(prompt)
                    
                    if not analysis_result:
                        analysis_result = self._generate_generic_analysis(prompt)
                    
                    st.session_state.ia_analysis_result = analysis_result
                    st.success("✅ Análise concluída!")
        
        # Preview de padrões detectados
        text_to_analyze = segment.get('text', '')[:3000]
        if text_to_analyze:
            patterns = self._analyze_text_patterns(text_to_analyze)
            
            with st.expander("🔍 Visualizar Padrões Detectados", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    if patterns['frequent_words']:
                        st.write("**📊 Palavras frequentes:**")
                        for word, count in list(patterns['frequent_words'].items())[:4]:
                            st.write(f"- `{word}`: {count}x")
                
                with col2:
                    if patterns['extended_themes']:
                        relevant_themes = {theme: score for theme, score in patterns['extended_themes'].items() if score > 5}
                        if relevant_themes:
                            st.write("**🌍 Temas detectados:**")
                            for theme, score in list(relevant_themes.items())[:3]:
                                st.write(f"- `{theme}`: {score:.1f}%")
        
        # Exibir resultado da análise
        if 'ia_analysis_result' in st.session_state and st.session_state.ia_analysis_result:
            st.markdown("---")
            st.subheader("📋 Resultado da Análise")
            st.markdown(st.session_state.ia_analysis_result)
            
    def _generate_contextual_prompt(self, prompt_type, text, segment):
        """Gera prompt contextualizado baseado no tipo de análise"""
        book_name = self.analysis_data.get('book_name', 'este livro')
        current_page = st.session_state.current_page
        current_chapter = self._get_current_chapter()
        
        chapter_info = f"Capítulo {current_chapter['number']}: {current_chapter['title']}" if current_chapter else "Contexto geral"
        
        prompts = {
            'page_summary': f"""Gere um resumo detalhado da página {current_page} do livro "{book_name}".
Contexto: {chapter_info}
Texto: {text[:2000]}
Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro.""",
            
            'analysis': f"""Analise profundamente este texto considerando:
1. Contexto histórico e significado filosófico
2. Metáforas, simbolismos e linguagem figurada  
3. Relações com temas maiores da obra
4. Implicações científicas, filosóficas ou sociais
5. Conexões com outros conceitos apresentados no livro

Contexto: {chapter_info}
Livro: {book_name}
Texto para análise: {text[:2000]}""",
            
            'explain_concepts': f"""Explique os conceitos complexos presentes no texto:
Contexto: {chapter_info}
Livro: {book_name}
Texto: {text[:2000]}
Forneça definições claras, exemplos práticos e relação com o contexto do livro.""",
            
            'chapter_context': f"""Considerando que este texto faz parte do {chapter_info} do livro "{book_name}",
analise como este trecho se relaciona com:
1. O contexto geral do capítulo
2. A estrutura narrativa do livro  
3. Os temas principais da obra
4. O desenvolvimento de ideias ao longo do livro

Trecho para análise: {text[:2000]}"""
        }
        
        return prompts.get(prompt_type, f"Analise o seguinte texto: {text[:2000]}")

    def _render_insights_tab(self, segment):
        st.subheader("🔍 Insights Automáticos")
        
        insights = self._generate_insights(segment)
        
        if insights:
            st.info("💡 **Insights detectados:**")
            for insight in insights[:3]:  # Limitar a 3 insights principais
                st.write(f"• {insight}")
            
            if len(insights) > 3:
                with st.expander("Ver mais insights"):
                    for insight in insights[3:]:
                        st.write(f"• {insight}")
            
            insights_text = "\n".join(insights)
            if st.button("📋 Copiar Insights", use_container_width=True):
                self._copy_to_clipboard(insights_text)
                st.success("✅ Insights copiados!")
        else:
            st.info("🤔 Nenhum insight automático detectado.")
        
        # Análise de padrões compacta
        st.markdown("---")
        st.subheader("📊 Análise Rápida")
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if text_analysis['frequent_words']:
                st.write("**🔤 Palavras-chave:**")
                for word, count in list(text_analysis['frequent_words'].items())[:4]:
                    st.write(f"`{word}` ({count}x)")
        
        with col2:
            if text_analysis['extended_themes']:
                relevant_themes = {t: s for t, s in text_analysis['extended_themes'].items() if s > 5}
                if relevant_themes:
                    st.write("**🎯 Temas:**")
                    for theme, score in list(relevant_themes.items())[:2]:
                        st.write(f"`{theme}`: {score:.1f}%")

    def _render_notes_tab(self):
        st.subheader("📝 Anotações Pessoais")
        
        # Área de nova anotação
        new_note = st.text_area(
            "✍️ Nova anotação:",
            placeholder="Digite suas anotações aqui...",
            height=120,
            key=f"new_note_{st.session_state.current_page}"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("💾 Salvar", use_container_width=True) and new_note:
                st.session_state.user_notes[st.session_state.current_page] = new_note
                st.success("✅ Salvo!")
        
        with col2:
            if st.button("🧹 Limpar", use_container_width=True):
                st.session_state.user_notes[st.session_state.current_page] = ""
        
        # Anotações salvas
        st.markdown("---")
        st.subheader("📓 Anotações Salvas")
        
        current_notes = st.session_state.user_notes.get(st.session_state.current_page, "")
        if current_notes.strip():
            st.text_area(
                f"Anotação Página {st.session_state.current_page}:",
                value=current_notes,
                height=200,
                key=f"current_note_display"
            )
        else:
            st.info("📝 Nenhuma anotação para esta página.")

    def _render_highlights_tab(self):
        st.subheader("⭐ Textos Destacados")
        
        current_page = st.session_state.current_page
        page_highlights = st.session_state.user_highlights.get(current_page, {})
        
        if page_highlights:
            st.success(f"📖 **{len(page_highlights)} destaque(s)**")
            
            for highlight_id, highlight_data in list(page_highlights.items())[:3]:  # Limitar a 3
                with st.expander(f"🔖 Destaque {list(page_highlights.keys()).index(highlight_id) + 1}", expanded=False):
                    st.info(f'"{highlight_data["text"]}"')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📋 Copiar", key=f"copy_{highlight_id}"):
                            self._copy_to_clipboard(highlight_data["text"])
                            st.success("✅ Copiado!")
                    with col2:
                        if st.button(f"🗑️ Remover", key=f"remove_{highlight_id}"):
                            del st.session_state.user_highlights[current_page][highlight_id]
                            st.success("✅ Removido!")
            
            if len(page_highlights) > 3:
                with st.expander("Ver todos os destaques"):
                    for highlight_id, highlight_data in list(page_highlights.items())[3:]:
                        st.info(f'"{highlight_data["text"]}"')
        else:
            st.info("⭐ Nenhum texto destacado nesta página.")
        
        # Estatísticas rápidas
        total_highlights = sum(len(highlights) for highlights in st.session_state.user_highlights.values())
        if total_highlights > 0:
            st.markdown("---")
            st.metric("📊 Total no livro", total_highlights)
            
    def _copy_to_clipboard(self, text):
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except:
            try:
                js_code = f"""
                navigator.clipboard.writeText(`{text}`).then(() => {{
                    console.log('Texto copiado para a área de transferência');
                }}).catch(err => {{
                    console.error('Erro ao copiar texto: ', err);
                }});
                """
                st.components.v1.html(f"<script>{js_code}</script>", height=0)
                return True
            except:
                st.error("❌ Não foi possível copiar para a área de transferência")
                return False
        
    def _generate_insights(self, segment):
        insights = []
        difficulty = segment.get('difficulty', 0)
        themes = segment.get('themes', {})
        readability = segment.get('analysis', {}).get('readability_score', 0)
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        extended_themes = text_analysis.get('extended_themes', {})
        
        if difficulty > 70:
            insights.append("💡 **Alta complexidade conceptual**: Esta página contém conceitos avançados de filosofia e ciência. Considere ler com atenção extra e fazer pausas para reflexão.")
        elif difficulty < 30:
            insights.append("💡 **Leitura acessível**: Conteúdo de fácil compreensão. Ideal para revisão rápida e absorção de conceitos fundamentais.")
        
        if themes:
            main_theme = max(themes, key=themes.get) if themes else None
            if main_theme:
                insights.append(f"🎯 **Tema principal**: {main_theme} ({themes[main_theme]:.1f}% de relevância). Este tema é central para a compreensão do capítulo atual.")
        
        for theme, score in extended_themes.items():
            if score > 20:
                icons = {'política': '🏛️', 'religião': '🙏', 'sexo': '❤️', 'cultura': '🎭'}
                insights.append(f"{icons.get(theme, '📊')} **Tema {theme}**: Forte presença ({score:.1f}%) - relevante para análise social do conteúdo.")
        
        if readability > 80:
            insights.append("📖 **Excelente legibilidade**: Texto bem estruturado e de fácil leitura. Aproveite para absorver os conceitos rapidamente.")
        elif readability < 50:
            insights.append("⚠️ **Texto complexo**: Estrutura de frases mais complexa. Considere ler em voz alta para melhor compreensão.")
        
        text = segment.get('text', '').lower()
        if any(word in text for word in ['tesla', 'energia', 'elétrica']):
            insights.append("🔌 **Contexto científico**: Esta página faz referência a conceitos de física e energia. Esses conceitos são usados como metáfora para processos conscientes.")
        
        if any(word in text for word in ['comportamento', 'humano', 'evolução']):
            insights.append("🧠 **Análise comportamental**: O texto explora padrões de comportamento humano. Preste atenção nas conexões entre biologia e psicologia.")
        
        return insights

    def _render_selected_text_analysis(self):
        if hasattr(st.session_state, 'show_ia_analysis') and st.session_state.show_ia_analysis:
            st.markdown("---")
            st.header("🧠 Análise Avançada do Texto Selecionado")
            
            selected_text = st.session_state.selected_text_for_analysis
            current_segment = self.segments[st.session_state.current_page - 1]
            context_text = current_segment.get('text', '')
            
            prompt = self._generate_text_analysis_prompt('analysis', selected_text)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**📝 Texto Selecionado para Análise:**")
                st.info(f'"{selected_text}"')
            
            with col2:
                if st.button("🔄 Gerar Nova Análise", use_container_width=True):
                    st.session_state.ia_analysis_result = None
                
                if st.button("❌ Fechar Análise", use_container_width=True):
                    st.session_state.show_ia_analysis = False
            
            patterns = self._analyze_text_patterns(selected_text)
            with st.expander("🔍 Padrões Detectados no Texto", expanded=False):
                if patterns['frequent_words']:
                    st.write("**📊 Palavras-chave:**")
                    for word, count in list(patterns['frequent_words'].items())[:5]:
                        st.write(f"- `{word}` ({count}x)")
                
                extended_themes = patterns.get('extended_themes', {})
                relevant_themes = {t: s for t, s in extended_themes.items() if s > 10}
                if relevant_themes:
                    st.write("**🌍 Temas Detectados:**")
                    for theme, score in relevant_themes.items():
                        st.write(f"- `{theme}`: {score:.1f}%")
            
            if 'ia_analysis_result' not in st.session_state:
                with st.spinner("🤖 Analisando texto com IA multidimensional..."):
                    analysis_result = self._call_deepseek_api(prompt)
                    st.session_state.ia_analysis_result = analysis_result
                    st.session_state.ia_prompt_used = prompt
            
            if st.session_state.ia_analysis_result:
                st.markdown("---")
                st.subheader("📋 Resultado da Análise Multidimensional")
                st.markdown(st.session_state.ia_analysis_result)
                
                with st.expander("🔧 Detalhes Técnicos da Análise"):
                    st.text_area("Prompt utilizado:", st.session_state.ia_prompt_used, height=200)
            
            st.markdown("---")
    
    def _render_segment_safely(self, segment):
        try:
            if not segment:
                st.warning("📄 Segmento não disponível")
                return
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                self._render_interactive_text(segment)
                
            with col2:
                self._render_analysis_tools(segment)
            
            self._render_visual_analysis(segment)
            
            self._render_selected_text_analysis()
            
        except Exception as e:
            st.error(f"❌ Erro ao renderizar página: {str(e)}")
            st.info("📋 Recarregue a página ou volte para a página anterior")

    def render_quantum_reader(self):
        """
        Renderiza o conteúdo principal da página atual do livro.
        """
        # ✅ Verificar se há uma mudança de página pendente
        if hasattr(st.session_state, 'pending_page') and st.session_state.pending_page != st.session_state.current_page:
            st.warning(f"📖 Página {st.session_state.pending_page} selecionada. Clique em 'Confirmar Mudança de Página' na sidebar para carregar.")
        
        # CORREÇÃO: Forçar rerun quando a página mudar (mantido para compatibilidade)
        if 'last_page' not in st.session_state:
            st.session_state.last_page = st.session_state.current_page
        
        if st.session_state.last_page != st.session_state.current_page:
            st.session_state.last_page = st.session_state.current_page
            st.rerun()
            
        if not self.render_controller.should_render():
            st.info("⏳ Carregando conteúdo...")
            return
            
        if not self.render_controller.acquire_lock():
            return
        
        try:
            current_page = st.session_state.current_page
            total_pages = len(self.segments)
            
            # CORREÇÃO: Verificar limites antes de renderizar
            if current_page > total_pages:
                st.session_state.current_page = total_pages
                st.rerun()
                return
                
            if current_page < 1:
                st.session_state.current_page = 1
                st.rerun()
                return
            
            # CORREÇÃO: Usar state_manager para obter segmento atual
            segment = self.state_manager.get_current_segment()
            
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; 
                        background: rgba(157, 78, 221, 0.1); padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; border-left: 4px solid #9d4edd;'>
                <div>
                    <h2 style='color: #e0aaff; margin: 0; font-size: 1.8rem;'>📖 {self.analysis_data.get('book_name', 'Livro')}</h2>
                    <p style='color: #c77dff; margin: 0;'>Página {current_page} de {total_pages}</p>
                </div>
                <div style='text-align: right;'>
                    <p style='color: #c77dff; margin: 0;'>Dificuldade: {segment.get('difficulty', 0):.1f}/100</p>
                    <p style='color: #c77dff; margin: 0;'>{segment.get('complexity_metrics', {}).get('word_count', 0)} palavras</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # CORREÇÃO: Chamar método de renderização seguro
            self._render_segment_safely(segment)
            
        except Exception as e:
            st.error(f"Erro na renderização: {e}")
            # CORREÇÃO: Definir segment antes de usar no except
            segment = self.state_manager.get_current_segment() if hasattr(self, 'state_manager') else {}
            if segment and 'text' in segment:
                st.text_area("Conteúdo da página:", segment['text'], height=300)
        finally:
            self.render_controller.release_lock()

    def render_book_overview(self):
        st.title("📊 Visão Geral do Livro")
        
        book_analysis = self.analysis_data.get('book_analysis', {})
        theme_analysis = self.analysis_data.get('theme_analysis', {})
        
        st.subheader("📈 Métricas Principais")
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("📄 Total de Páginas", book_analysis.get('total_segments', 0), "#4cc9f0"),
            ("📝 Palavras", book_analysis.get('total_words', 0), "#9d4edd"),
            ("🎯 Dificuldade Média", f"{book_analysis.get('avg_difficulty', 0):.1f}/100", "#ff9800"),
            ("📈 Variação", f"{book_analysis.get('max_difficulty', 0) - book_analysis.get('min_difficulty', 0):.1f}", "#f44336")
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class='metric-card pulse-animation'>
                    <h3 style='color: {color}; margin: 0; font-size: 1.2rem;'>{label}</h3>
                    <p style='font-size: 2.2rem; font-weight: bold; color: {color}; margin: 0;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📊 Evolução da Dificuldade")
        difficulties = [s.get('difficulty', 0) for s in self.segments]
        
        if difficulties:
            df = pd.DataFrame({
                'Página': range(1, len(difficulties) + 1),
                'Dificuldade': difficulties,
                'Capítulo': ['Geral'] * len(difficulties)
            })
            
            if self.chapters:
                for i, chapter in enumerate(self.chapters):
                    start, end = chapter['start_page'] - 1, min(chapter['end_page'], len(difficulties))
                    df.loc[start:end, 'Capítulo'] = f"Cap {chapter['number']}"
            
            fig = px.line(df, x='Página', y='Dificuldade', 
                        title="Evolução da Dificuldade por Página",
                        color='Capítulo',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            avg_difficulty = book_analysis.get('avg_difficulty', 0)
            fig.add_hline(y=avg_difficulty, 
                        line_dash="dash", line_color="red",
                        annotation_text=f"Média: {avg_difficulty:.1f}")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0aaff'),
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        if theme_analysis:
            st.markdown("---")
            st.subheader("🎭 Mapa de Calor Temático")
            
            extended_theme_analysis = {}
            for theme_name in self.extended_themes.keys():
                extended_theme_analysis[theme_name] = []
            
            for i, segment in enumerate(self.segments):
                text = segment.get('text', '')
                segment_themes = self._analyze_extended_themes(text)
                
                for theme_name, score in segment_themes.items():
                    extended_theme_analysis[theme_name].append({
                        'segment': i + 1,
                        'score': score
                    })
            
            combined_theme_analysis = {**theme_analysis, **extended_theme_analysis}
            
            theme_names = list(combined_theme_analysis.keys())
            max_pages = max(len(data) for data in combined_theme_analysis.values())
            
            heatmap_data = []
            for theme in theme_names:
                theme_scores = [0] * max_pages
                for point in combined_theme_analysis[theme]:
                    if point['segment'] <= max_pages:
                        theme_scores[point['segment'] - 1] = point['score']
                heatmap_data.append(theme_scores)
            
            fig = px.imshow(heatmap_data,
                        labels=dict(x="Página", y="Tema", color="Intensidade"),
                        x=list(range(1, max_pages + 1)),
                        y=theme_names,
                        aspect="auto",
                        color_continuous_scale="viridis")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0aaff'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🌍 Análise de Temas Sociais e Culturais")
        
        all_text = " ".join([segment.get('text', '') for segment in self.segments])
        extended_themes = self._analyze_extended_themes(all_text)
        
        if extended_themes:
            theme_cols = st.columns(4)
            
            for i, (theme, score) in enumerate(extended_themes.items()):
                if score > 5:
                    with theme_cols[i % 4]:
                        icons = {
                            'política': '🏛️',
                            'religião': '🙏',
                            'sexo': '❤️',
                            'cultura': '🎭'
                        }
                        
                        st.metric(
                            label=f"{icons.get(theme, '📊')} {theme.capitalize()}",
                            value=f"{score:.1f}%",
                            help=f"Intensidade do tema {theme} no livro"
                        )
            
            if any(score > 5 for score in extended_themes.values()):
                extended_df = pd.DataFrame({
                    'Tema': list(extended_themes.keys()),
                    'Intensidade': list(extended_themes.values())
                }).sort_values('Intensidade', ascending=False)
                
                fig = px.bar(extended_df, x='Tema', y='Intensidade',
                            title="📊 Intensidade dos Temas Sociais no Livro",
                            color='Intensidade',
                            color_continuous_scale='viridis')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🤔 Nenhum tema social significativo detectado no livro.")
        
        st.markdown("---")
        st.subheader("🧠 Estatísticas de Leitura")
        
        total_words = book_analysis.get('total_words', 0)
        reading_time_min = total_words / 200
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("⏱️ Tempo Estimado", f"{reading_time_min:.0f} min")
        
        with stat_col2:
            avg_difficulty = book_analysis.get('avg_difficulty', 0)
            level = "Fácil" if avg_difficulty < 40 else "Médio" if avg_difficulty < 70 else "Difícil"
            st.metric("📊 Nível", level)
        
        with stat_col3:
            st.metric("📖 Densidade", f"{(total_words/book_analysis.get('total_segments', 1)):.0f} palavras/página")
    
    def render_export_section(self):
        st.title("💾 Exportar Dados e Relatórios")
        
        st.info("""
        **Exporte seus dados de leitura** para análise externa, compartilhamento ou backup.
        Todos os relatórios incluem suas anotações pessoais e destaques.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Dados de Análise")
            
            if st.button("📄 JSON Completo", use_container_width=True, help="Exportar todos os dados de análise em formato JSON"):
                try:
                    export_data = self.analysis_data.copy()
                    export_data['user_notes'] = st.session_state.user_notes
                    export_data['user_highlights'] = st.session_state.user_highlights

                    data_str = safe_json_dump(export_data)

                    b64 = base64.b64encode(data_str.encode()).decode()
                    href = f'<a href="data:application/json;base64,{b64}" download="analise_livro_completa.json">⬇️ Baixar JSON Completo</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao gerar JSON: {str(e)}")
            
            if st.button("📈 Dados Estatísticos", use_container_width=True, help="Exportar métricas e estatísticas em CSV"):
                try:
                    output = "Página,Dificuldade,Palavras,Sentenças,Tema Principal\n"
                    for i, segment in enumerate(self.segments):
                        themes = segment.get('themes', {})
                        main_theme = max(themes, key=themes.get) if themes else 'Nenhum'
                        output += f"{i + 1},{segment.get('difficulty', 0)},{segment.get('complexity_metrics', {}).get('word_count', 0)},{segment.get('complexity_metrics', {}).get('sentence_count', 0)},{main_theme}\n"
                    
                    b64 = base64.b64encode(output.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="estatisticas_livro.csv">⬇️ Baixar CSV Estatístico</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao gerar CSV: {str(e)}")
        
        with col2:
            st.subheader("📝 Conteúdo Personalizado")
            
            if st.button("📖 Anotações Pessoais", use_container_width=True, help="Exportar apenas suas anotações e destaques"):
                self._export_notes()
            
            if st.button("🖼️ Gráficos de Análise", use_container_width=True, help="Exportar visualizações gráficas (em breve)"):
                st.info("Recurso em desenvolvimento - em breve disponível!")
            
            if st.button("🤖 Análises com IA", use_container_width=True, help="Exportar análises geradas pela IA (em breve)"):
                st.info("Recurso em desenvolvimento - em breve disponível!")
    
    def _export_notes(self):
        if not st.session_state.user_notes:
            st.warning("Não há anotações para exportar.")
            return
        
        notes_text = "# Anotações Pessoais - FLUX-ON Reader\n\n"
        for page, note in st.session_state.user_notes.items():
            if note.strip():
                notes_text += f"## Página {page}\n\n{note}\n\n---\n\n"
        
        b64 = base64.b64encode(notes_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="anotacoes_fluxon.txt">📥 Baixar Anotações</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("Anotações preparadas para download!")

    def render(self):
        if 'book_cover_shown' not in st.session_state:
            book_cover = self.analysis_data.get('book_cover')
            if book_cover:
                st.markdown("""
                <div style='text-align: center; margin: 2rem 0; padding: 2rem; background: rgba(45, 45, 65, 0.8); border-radius: 20px;'>
                    <h1 style='color: #e0aaff; margin-bottom: 2rem;'>📖 {}</h1>
                    <img src="{}" style="max-width: 300px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                </div>
                """.format(self.analysis_data.get('book_name', 'Livro'), book_cover), 
                unsafe_allow_html=True)
                
                st.markdown("---")
                st.session_state.book_cover_shown = True
        
        self.render_search_interface()
        
        # Adicionar opção de menu para resultados de busca
        menu_options = {
            "📖 Ler Livro": self.render_quantum_reader,
            "📊 Visão Geral": self.render_book_overview,
            "🔍 Resultados Busca": self.render_search_results_page,  # NOVO
            "🔧 Configurações": self._render_api_configuration,
            "💾 Exportar": self.render_export_section
        }
        
        with st.sidebar:
            selected_menu = st.selectbox(
                "**Navegação Principal**",
                list(menu_options.keys()),
                index=0
            )
        
        self.render_advanced_sidebar()
        
        menu_options[selected_menu]()
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #c77dff; padding: 2rem; background: rgba(157, 78, 221, 0.1); border-radius: 15px;'>
            <p style='font-size: 1.2rem; margin-bottom: 0.5rem;'>✨ <strong>FLUX-ON Quantum Reader v8.0</strong> - Sistema Avançado de Análise Literária</p>
            <p style='margin: 0;'>📚 Transformando leitura em experiência quântica multidimensional</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    try:
        if 'book_loaded' not in st.session_state:
            st.session_state.book_loaded = False
        
        if not st.session_state.book_loaded:
            render_book_opener()
            return
            
        analysis_data_str = """{
  "book_analysis": {
    "total_segments": 159,
    "total_chapters": 26,
    "total_pages": 159,
    "avg_difficulty": 31.982159598080692,
    "max_difficulty": 47.781168831168834,
    "min_difficulty": 18.55,
    "theme_distribution": {
      "filosofia": 82.0032223415682,
      "ciencia": 83.71608368747957,
      "arte": 71.66666666666667,
      "tecnologia": 34.89702517162471
    },
    "total_words": 25490,
    "avg_words_per_segment": 160.31446540880503,
    "formatting_preservation": 79.62264150943396,
    "preservation_score": 1.4014427764953052e-05,
    "book_name": "O_Presidente_diagramado 1.pdf",
    "analysis_timestamp": "2025-09-15T19:00:17",
    "structure_preserved": false
  },
  "theme_analysis": {
    "filosofia": [
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 1577,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 9776,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 19522,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 43024,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 49507,
        "chapter": 11
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 52071,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 75.0,
        "position": 103079,
        "chapter": 21
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 111488,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 39.473684210526315,
        "position": 128078,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 129402,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 133024,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 141868,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 152526,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 156699,
        "chapter": 7
      }
    ],
    "ciencia": [
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 1577,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 10976,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 44304,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 48520,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 54481,
        "chapter": 12
      },
      {
        "segment": 1,
        "score": 34.21052631578947,
        "position": 128078,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 134349,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 139849,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 148046,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 171023,
        "chapter": 8
      }
    ],
    "arte": [
      {
        "segment": 1,
        "score": 40.0,
        "position": 9776,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 30667,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 66349,
        "chapter": 14
      },
      {
        "segment": 1,
        "score": 25.0,
        "position": 103079,
        "chapter": 21
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 141868,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 155711,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 156699,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 160755,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 165824,
        "chapter": 7
      }
    ],
    "tecnologia": [
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 54481,
        "chapter": 12
      },
      {
        "segment": 1,
        "score": 26.31578947368421,
        "position": 128078,
        "chapter": 5
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 36.13543689320388,
      "position": 274,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 9.298047464489666e-06
    },
    {
      "segment": 1,
      "difficulty": 35.08274336283186,
      "position": 1577,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 226,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 38.453591160220995,
      "position": 2968,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 181,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 32.643846153846155,
      "position": 4197,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 65,
      "preservation_score": 1.5810445081318458e-06
    },
    {
      "segment": 1,
      "difficulty": 36.41754385964912,
      "position": 4706,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 8.808676545305998e-06
    },
    {
      "segment": 1,
      "difficulty": 20.7625,
      "position": 5882,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 16,
      "preservation_score": 1.8821958430141024e-07
    },
    {
      "segment": 1,
      "difficulty": 23.62574780058651,
      "position": 6157,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 36.307575757575755,
      "position": 7303,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 198,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 31.692622950819672,
      "position": 8571,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 2.0741798190015406e-05
    },
    {
      "segment": 1,
      "difficulty": 30.262417582417584,
      "position": 9776,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 195,
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "segment": 1,
      "difficulty": 30.751172707889125,
      "position": 10976,
      "chapter": 1,
      "main_theme": "ciencia",
      "word_count": 201,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 35.30921052631579,
      "position": 12255,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 5.383080111020332e-06
    },
    {
      "segment": 1,
      "difficulty": 28.40342105263158,
      "position": 13278,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 190,
      "preservation_score": 1.8069080092935382e-05
    },
    {
      "segment": 1,
      "difficulty": 30.197229729729727,
      "position": 14617,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 185,
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "segment": 1,
      "difficulty": 33.116934046345804,
      "position": 15879,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 187,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 31.17787794729542,
      "position": 17116,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "segment": 1,
      "difficulty": 26.869642857142857,
      "position": 18472,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 168,
      "preservation_score": 1.4078824905745484e-05
    },
    {
      "segment": 1,
      "difficulty": 35.78048780487805,
      "position": 19522,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 205,
      "preservation_score": 1.4229400573186614e-05
    },
    {
      "segment": 1,
      "difficulty": 36.356818181818184,
      "position": 20816,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 220,
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "segment": 1,
      "difficulty": 32.83360655737705,
      "position": 22173,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 61,
      "preservation_score": 1.5810445081318458e-06
    },
    {
      "segment": 1,
      "difficulty": 31.331638418079095,
      "position": 22707,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 177,
      "preservation_score": 1.0728516305180385e-05
    },
    {
      "segment": 1,
      "difficulty": 35.77463768115942,
      "position": 23953,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 207,
      "preservation_score": 2.6350741802197434e-05
    },
    {
      "segment": 1,
      "difficulty": 31.03121387283237,
      "position": 25352,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "segment": 1,
      "difficulty": 25.433333333333334,
      "position": 26555,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 36,
      "preservation_score": 6.775905034850767e-07
    },
    {
      "segment": 1,
      "difficulty": 47.781168831168834,
      "position": 26938,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 1.0239145385996715e-05
    },
    {
      "segment": 1,
      "difficulty": 29.83712121212121,
      "position": 28060,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 198,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 27.931206804891016,
      "position": 29364,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 209,
      "preservation_score": 1.897253409758215e-05
    },
    {
      "segment": 1,
      "difficulty": 27.16760355029586,
      "position": 30667,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 169,
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "segment": 1,
      "difficulty": 31.059163763066202,
      "position": 31846,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 205,
      "preservation_score": 1.8596094928979333e-05
    },
    {
      "segment": 1,
      "difficulty": 30.482853982300885,
      "position": 33111,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 226,
      "preservation_score": 2.108059344175795e-05
    },
    {
      "segment": 1,
      "difficulty": 36.059615384615384,
      "position": 34548,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 156,
      "preservation_score": 1.084144805576123e-05
    },
    {
      "segment": 1,
      "difficulty": 37.73228476821192,
      "position": 35855,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 151,
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "segment": 1,
      "difficulty": 30.162723214285712,
      "position": 37007,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 192,
      "preservation_score": 1.2874219566216461e-05
    },
    {
      "segment": 1,
      "difficulty": 35.740932642487046,
      "position": 38268,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 193,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 34.339335664335664,
      "position": 39531,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 143,
      "preservation_score": 8.432237376703178e-06
    },
    {
      "segment": 1,
      "difficulty": 29.39327731092437,
      "position": 40523,
      "chapter": 9,
      "main_theme": "none",
      "word_count": 187,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 28.021195652173915,
      "position": 41766,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "segment": 1,
      "difficulty": 32.4088132635253,
      "position": 43024,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 191,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 32.84710884353741,
      "position": 44304,
      "chapter": 2,
      "main_theme": "ciencia",
      "word_count": 196,
      "preservation_score": 2.002656376967005e-05
    },
    {
      "segment": 1,
      "difficulty": 33.440453074433655,
      "position": 45627,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 23.184615384615384,
      "position": 46978,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 13,
      "preservation_score": 1.1293175058084612e-07
    },
    {
      "segment": 1,
      "difficulty": 35.34550561797753,
      "position": 47242,
      "chapter": 10,
      "main_theme": "none",
      "word_count": 178,
      "preservation_score": 1.21589851458711e-05
    },
    {
      "segment": 1,
      "difficulty": 30.406474820143885,
      "position": 48520,
      "chapter": 2,
      "main_theme": "ciencia",
      "word_count": 139,
      "preservation_score": 7.90522254065923e-06
    },
    {
      "segment": 1,
      "difficulty": 33.026993865030676,
      "position": 49507,
      "chapter": 11,
      "main_theme": "filosofia",
      "word_count": 163,
      "preservation_score": 2.168289611152246e-05
    },
    {
      "segment": 1,
      "difficulty": 32.90035360678925,
      "position": 50737,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 27.495454545454546,
      "position": 52071,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 198,
      "preservation_score": 2.574843913243292e-05
    },
    {
      "segment": 1,
      "difficulty": 31.157931034482758,
      "position": 53395,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 145,
      "preservation_score": 1.1293175058084614e-05
    },
    {
      "segment": 1,
      "difficulty": 32.86818181818182,
      "position": 54481,
      "chapter": 12,
      "main_theme": "ciencia",
      "word_count": 198,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 35.29620462046205,
      "position": 55763,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 28.08804347826087,
      "position": 57093,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 2.303807711849261e-05
    },
    {
      "segment": 1,
      "difficulty": 30.392239010989012,
      "position": 58392,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 1.4304688406907178e-05
    },
    {
      "segment": 1,
      "difficulty": 28.550064766839377,
      "position": 59765,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 193,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 22.027272727272727,
      "position": 61055,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 33,
      "preservation_score": 9.03454004646769e-07
    },
    {
      "segment": 1,
      "difficulty": 29.719585253456223,
      "position": 61404,
      "chapter": 13,
      "main_theme": "none",
      "word_count": 186,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 36.44731707317073,
      "position": 62650,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 205,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 30.7173007896626,
      "position": 63983,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 199,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 27.35014005602241,
      "position": 65319,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 9.486267048791075e-06
    },
    {
      "segment": 1,
      "difficulty": 32.4890625,
      "position": 66349,
      "chapter": 14,
      "main_theme": "arte",
      "word_count": 192,
      "preservation_score": 1.21589851458711e-05
    },
    {
      "segment": 1,
      "difficulty": 32.77948717948718,
      "position": 67673,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 195,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 33.84487179487179,
      "position": 68950,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "segment": 1,
      "difficulty": 35.40526315789474,
      "position": 70514,
      "chapter": 15,
      "main_theme": "none",
      "word_count": 190,
      "preservation_score": 1.0163857552276153e-05
    },
    {
      "segment": 1,
      "difficulty": 31.711764705882352,
      "position": 71769,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 1.325065873481928e-05
    },
    {
      "segment": 1,
      "difficulty": 35.17627118644067,
      "position": 72840,
      "chapter": 16,
      "main_theme": "none",
      "word_count": 177,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 30.35434462444772,
      "position": 74068,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 194,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 27.743333333333332,
      "position": 75325,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 45,
      "preservation_score": 6.023026697645126e-07
    },
    {
      "segment": 1,
      "difficulty": 36.38938547486033,
      "position": 75924,
      "chapter": 17,
      "main_theme": "none",
      "word_count": 179,
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "segment": 1,
      "difficulty": 22.520721153846154,
      "position": 77116,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 160,
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "segment": 1,
      "difficulty": 29.596153846153847,
      "position": 78155,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 1.490699107667169e-05
    },
    {
      "segment": 1,
      "difficulty": 29.79050193050193,
      "position": 79403,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 185,
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "segment": 1,
      "difficulty": 33.531952117863725,
      "position": 80699,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 181,
      "preservation_score": 1.897253409758215e-05
    },
    {
      "segment": 1,
      "difficulty": 34.5944099378882,
      "position": 81896,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 161,
      "preservation_score": 9.034540046467691e-06
    },
    {
      "segment": 1,
      "difficulty": 25.579779158040026,
      "position": 83006,
      "chapter": 18,
      "main_theme": "none",
      "word_count": 161,
      "preservation_score": 2.1005305608037384e-05
    },
    {
      "segment": 1,
      "difficulty": 25.31981599433829,
      "position": 84168,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 157,
      "preservation_score": 1.897253409758215e-05
    },
    {
      "segment": 1,
      "difficulty": 28.259625668449196,
      "position": 85280,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 187,
      "preservation_score": 1.7617353090611997e-05
    },
    {
      "segment": 1,
      "difficulty": 26.883841463414633,
      "position": 86552,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 164,
      "preservation_score": 1.5358718078995074e-05
    },
    {
      "segment": 1,
      "difficulty": 28.79081632653061,
      "position": 87724,
      "chapter": 19,
      "main_theme": "none",
      "word_count": 147,
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "segment": 1,
      "difficulty": 28.25040322580645,
      "position": 88808,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 186,
      "preservation_score": 2.145703261036077e-05
    },
    {
      "segment": 1,
      "difficulty": 30.138145100972324,
      "position": 90110,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 191,
      "preservation_score": 1.2874219566216461e-05
    },
    {
      "segment": 1,
      "difficulty": 32.665018315018315,
      "position": 91396,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "segment": 1,
      "difficulty": 30.276730486008837,
      "position": 92626,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 194,
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "segment": 1,
      "difficulty": 29.732488479262674,
      "position": 93879,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 186,
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "segment": 1,
      "difficulty": 26.4032196969697,
      "position": 95102,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 176,
      "preservation_score": 1.788086050863397e-05
    },
    {
      "segment": 1,
      "difficulty": 31.793852459016392,
      "position": 96341,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 122,
      "preservation_score": 1.1744902060407997e-05
    },
    {
      "segment": 1,
      "difficulty": 31.03875968992248,
      "position": 97199,
      "chapter": 20,
      "main_theme": "none",
      "word_count": 172,
      "preservation_score": 1.7316201755729746e-05
    },
    {
      "segment": 1,
      "difficulty": 35.49523809523809,
      "position": 98487,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 1.788086050863397e-05
    },
    {
      "segment": 1,
      "difficulty": 33.830462519936205,
      "position": 99760,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 209,
      "preservation_score": 3.162089016263692e-05
    },
    {
      "segment": 1,
      "difficulty": 31.25651872399445,
      "position": 101156,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 1.581044508131846e-05
    },
    {
      "segment": 1,
      "difficulty": 35.91538461538461,
      "position": 102559,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 39,
      "preservation_score": 7.905222540659229e-07
    },
    {
      "segment": 1,
      "difficulty": 27.935860655737706,
      "position": 103079,
      "chapter": 21,
      "main_theme": "filosofia",
      "word_count": 183,
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "segment": 1,
      "difficulty": 32.0370249017038,
      "position": 104355,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 218,
      "preservation_score": 1.8069080092935382e-05
    },
    {
      "segment": 1,
      "difficulty": 36.14114285714286,
      "position": 105777,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "segment": 1,
      "difficulty": 27.05188679245283,
      "position": 106996,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 106,
      "preservation_score": 6.023026697645128e-06
    },
    {
      "segment": 1,
      "difficulty": 31.75996376811594,
      "position": 107779,
      "chapter": 22,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 1.788086050863397e-05
    },
    {
      "segment": 1,
      "difficulty": 30.791472868217056,
      "position": 109024,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 172,
      "preservation_score": 1.2046053395290256e-05
    },
    {
      "segment": 1,
      "difficulty": 32.22936507936508,
      "position": 110184,
      "chapter": 23,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 29.526519337016573,
      "position": 111488,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 181,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 26.252586206896552,
      "position": 112735,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 116,
      "preservation_score": 1.0841448055761226e-05
    },
    {
      "segment": 1,
      "difficulty": 38.87717391304348,
      "position": 113745,
      "chapter": 24,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "segment": 1,
      "difficulty": 34.358566978193146,
      "position": 115017,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 214,
      "preservation_score": 2.1833471778963585e-05
    },
    {
      "segment": 1,
      "difficulty": 34.15428571428571,
      "position": 116459,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 35,
      "preservation_score": 3.387952517425383e-07
    },
    {
      "segment": 1,
      "difficulty": 32.77738095238095,
      "position": 116956,
      "chapter": 25,
      "main_theme": "none",
      "word_count": 196,
      "preservation_score": 1.788086050863397e-05
    },
    {
      "segment": 1,
      "difficulty": 32.84472789115647,
      "position": 118231,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 196,
      "preservation_score": 1.931132934932469e-05
    },
    {
      "segment": 1,
      "difficulty": 30.48469387755102,
      "position": 119506,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 196,
      "preservation_score": 2.2887501451051485e-05
    },
    {
      "segment": 1,
      "difficulty": 25.32586206896552,
      "position": 120809,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 174,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 30.160191846522782,
      "position": 122020,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 139,
      "preservation_score": 1.2648356065054767e-05
    },
    {
      "segment": 1,
      "difficulty": 33.67588235294117,
      "position": 123165,
      "chapter": 26,
      "main_theme": "none",
      "word_count": 170,
      "preservation_score": 2.145703261036077e-05
    },
    {
      "segment": 1,
      "difficulty": 34.358245614035084,
      "position": 124415,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 190,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 30.87708333333333,
      "position": 125664,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 144,
      "preservation_score": 1.5170498494693666e-05
    },
    {
      "segment": 1,
      "difficulty": 31.101724137931036,
      "position": 126803,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 174,
      "preservation_score": 2.217226703070613e-05
    },
    {
      "segment": 1,
      "difficulty": 32.69770279971285,
      "position": 128078,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 199,
      "preservation_score": 2.0741798190015406e-05
    },
    {
      "segment": 1,
      "difficulty": 30.779824561403508,
      "position": 129402,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 171,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 34.714814814814815,
      "position": 130588,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 1.558458158015677e-05
    },
    {
      "segment": 1,
      "difficulty": 29.27014563106796,
      "position": 131716,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 2.43179702917422e-05
    },
    {
      "segment": 1,
      "difficulty": 28.979,
      "position": 133024,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 200,
      "preservation_score": 2.2887501451051485e-05
    },
    {
      "segment": 1,
      "difficulty": 39.7609375,
      "position": 134349,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 192,
      "preservation_score": 2.0327715104552305e-05
    },
    {
      "segment": 1,
      "difficulty": 25.508333333333333,
      "position": 135692,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 36,
      "preservation_score": 4.517270023233845e-07
    },
    {
      "segment": 1,
      "difficulty": 24.921153846153846,
      "position": 136069,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 65,
      "preservation_score": 4.517270023233846e-06
    },
    {
      "segment": 1,
      "difficulty": 18.55,
      "position": 136603,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 2,
      "preservation_score": 0.0
    },
    {
      "segment": 1,
      "difficulty": 32.43018867924528,
      "position": 136779,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 159,
      "preservation_score": 1.65633234185241e-05
    },
    {
      "segment": 1,
      "difficulty": 28.11354916067146,
      "position": 137890,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 139,
      "preservation_score": 1.287421956621646e-05
    },
    {
      "segment": 1,
      "difficulty": 26.649250749250747,
      "position": 138876,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 143,
      "preservation_score": 9.486267048791075e-06
    },
    {
      "segment": 1,
      "difficulty": 31.341610738255035,
      "position": 139849,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 149,
      "preservation_score": 1.21589851458711e-05
    },
    {
      "segment": 1,
      "difficulty": 26.933396404919584,
      "position": 140861,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 151,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 31.21367041198502,
      "position": 141868,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 178,
      "preservation_score": 1.65633234185241e-05
    },
    {
      "segment": 1,
      "difficulty": 24.911764705882355,
      "position": 143003,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 17,
      "preservation_score": 1.5057566744112816e-07
    },
    {
      "segment": 1,
      "difficulty": 35.85557851239669,
      "position": 143369,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 121,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 36.0781914893617,
      "position": 144361,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 141,
      "preservation_score": 1.1443750725525743e-05
    },
    {
      "segment": 1,
      "difficulty": 38.55769230769231,
      "position": 145330,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 130,
      "preservation_score": 1.0728516305180385e-05
    },
    {
      "segment": 1,
      "difficulty": 23.214565826330535,
      "position": 146284,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 119,
      "preservation_score": 1.084144805576123e-05
    },
    {
      "segment": 1,
      "difficulty": 31.70121951219512,
      "position": 147178,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 123,
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "segment": 1,
      "difficulty": 36.527464788732395,
      "position": 148046,
      "chapter": 7,
      "main_theme": "ciencia",
      "word_count": 142,
      "preservation_score": 1.430468840690718e-05
    },
    {
      "segment": 1,
      "difficulty": 36.408029197080296,
      "position": 149053,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 137,
      "preservation_score": 7.039412452872742e-06
    },
    {
      "segment": 1,
      "difficulty": 29.391774891774894,
      "position": 149978,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 77,
      "preservation_score": 3.3879525174253846e-06
    },
    {
      "segment": 1,
      "difficulty": 36.493877551020404,
      "position": 150600,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 147,
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "segment": 1,
      "difficulty": 32.88549618320611,
      "position": 151642,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 131,
      "preservation_score": 9.486267048791075e-06
    },
    {
      "segment": 1,
      "difficulty": 36.532075471698114,
      "position": 152526,
      "chapter": 7,
      "main_theme": "filosofia",
      "word_count": 159,
      "preservation_score": 2.002656376967005e-05
    },
    {
      "segment": 1,
      "difficulty": 36.42792207792208,
      "position": 153636,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 1.0013281884835026e-05
    },
    {
      "segment": 1,
      "difficulty": 38.488157894736844,
      "position": 154664,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "segment": 1,
      "difficulty": 36.452413793103446,
      "position": 155711,
      "chapter": 7,
      "main_theme": "arte",
      "word_count": 145,
      "preservation_score": 1.21589851458711e-05
    },
    {
      "segment": 1,
      "difficulty": 36.40958904109589,
      "position": 156699,
      "chapter": 7,
      "main_theme": "filosofia",
      "word_count": 146,
      "preservation_score": 1.0163857552276153e-05
    },
    {
      "segment": 1,
      "difficulty": 38.448507462686564,
      "position": 157672,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 134,
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "segment": 1,
      "difficulty": 36.50185185185185,
      "position": 158600,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 2.1833471778963585e-05
    },
    {
      "segment": 1,
      "difficulty": 38.494039735099335,
      "position": 159709,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 151,
      "preservation_score": 9.298047464489666e-06
    },
    {
      "segment": 1,
      "difficulty": 38.3859649122807,
      "position": 160755,
      "chapter": 7,
      "main_theme": "arte",
      "word_count": 171,
      "preservation_score": 1.2798931732495895e-05
    },
    {
      "segment": 1,
      "difficulty": 35.96606060606061,
      "position": 161860,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 1.0013281884835026e-05
    },
    {
      "segment": 1,
      "difficulty": 36.43032258064516,
      "position": 162866,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 1.4229400573186614e-05
    },
    {
      "segment": 1,
      "difficulty": 38.43239436619719,
      "position": 163904,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 142,
      "preservation_score": 1.21589851458711e-05
    },
    {
      "segment": 1,
      "difficulty": 33.15205479452055,
      "position": 164867,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 146,
      "preservation_score": 1.8596094928979333e-05
    },
    {
      "segment": 1,
      "difficulty": 36.27582417582418,
      "position": 165824,
      "chapter": 7,
      "main_theme": "arte",
      "word_count": 182,
      "preservation_score": 1.581044508131846e-05
    },
    {
      "segment": 1,
      "difficulty": 38.41509433962264,
      "position": 166924,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 159,
      "preservation_score": 1.65633234185241e-05
    },
    {
      "segment": 1,
      "difficulty": 36.3796052631579,
      "position": 167983,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 9.486267048791075e-06
    },
    {
      "segment": 1,
      "difficulty": 36.37647058823529,
      "position": 168975,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "segment": 1,
      "difficulty": 37.56164383561644,
      "position": 169975,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 146,
      "preservation_score": 1.581044508131846e-05
    },
    {
      "segment": 1,
      "difficulty": 36.82589928057554,
      "position": 171023,
      "chapter": 8,
      "main_theme": "ciencia",
      "word_count": 139,
      "preservation_score": 2.7103620139403077e-05
    },
    {
      "segment": 1,
      "difficulty": 36.52517482517483,
      "position": 172146,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 143,
      "preservation_score": 9.787418383673333e-06
    },
    {
      "segment": 1,
      "difficulty": 36.38607594936709,
      "position": 173158,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 158,
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "segment": 1,
      "difficulty": 34.09255319148936,
      "position": 174187,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 141,
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "segment": 1,
      "difficulty": 23.35539568345324,
      "position": 175100,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 139,
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "segment": 1,
      "difficulty": 23.55,
      "position": 176021,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 30,
      "preservation_score": 6.775905034850767e-07
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Introdução    \\nDedicatória ao presidente   \\n  Logo no início do livro, venho te mostrando algumas das \\ndificuldades de ser presidente, ser um líder dessa magnitude o \\ndeixa frágil em momentos de fragilidade e o deixa forte em \\nmomentos fortes. O mesmo povo que quer evoluir com o país é o \\nmesmo povo que q uer viver com o luxo para si próprio, o que me \\nfaz perceber a necessidade de conhecer o povo para o qual você é \\nlíder e, através deste livro, encontrar uma forma de tentar \\ncompreender o incompreensível e tentar escrever de uma forma \\nmais clara e acessível a todos que aqui habitam.    \\nQuase todos que aqui habitam só enxergam as \\ndificuldades das suas próprias vidas, deixando de ver que o seu \\ntrabalho é igual ao dele. O modo de viver é igual ao dele que está \\nte criticando ou até mesmo agredindo sem nem mesmo s aber das \\ndificuldades atreladas ao cargo o qual está exercendo. Esse cargo \\nque você só está devido à maioria enxergá -lo como um líder a ser \\nseguido é o mesmo que irá te consumir por um trabalho que \\nninguém sabe fazer, onde todos sabem resolver todos os \\nproblemas diante do seu próprio viver, sem saber viver o seu",
      "position": 274,
      "chapter": 1,
      "page": 2,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.13543689320388,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 41.2,
        "avg_word_length": 4.432038834951456,
        "unique_word_ratio": 0.5922330097087378,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.05825242718446602,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mesmo",
          "viver",
          "todos",
          "dificuldades",
          "líder",
          "povo",
          "está",
          "presidente",
          "livro",
          "deixa",
          "momentos",
          "próprio",
          "qual",
          "você",
          "forma",
          "tentar",
          "aqui",
          "habitam",
          "trabalho",
          "igual"
        ],
        "entities": [
          [
            "Introdução",
            "ORG"
          ],
          [
            "Dedicatória",
            "ORG"
          ],
          [
            "algumas das \\ndificuldades de ser presidente",
            "PERSON"
          ],
          [
            "deixa frágil em momentos de fragilidade e",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "evoluir",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "de uma forma",
            "PERSON"
          ],
          [
            "mais clara",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 78.07038834951456,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 122,
        "lexical_diversity": 0.5922330097087378
      },
      "preservation_score": 9.298047464489666e-06
    },
    {
      "id": 1,
      "text": "próprio viver, assim tornando o seu trabalho em ser presidente um \\ntrabalho impossível de ser executado com excelência.    \\nLogo, eu vejo a necessidade de reconhecer a maior \\nquantidade de pessoas que querem uma direção de um viver \\nmelhor, através deste pequeno livro baseado na obra “ O \\nPríncipe”,  de Maquiavel . Tento fazer algo que possa melhorar \\num pouco nosso viver, sei que estou sendo muito prepotente ou \\naté mesmo arrogante em querer direcionar alguém  como o senhor, \\npresidente, pois sei que tem uma grandeza a qual eu não sei viver, \\nmuito menos irei saber viver e não quero saber viver essa \\ngrandeza. Tenho um estilo de vida o qual vejo não saber viver \\nessa liderança e tenho consciência de que, quando é b em exercida, \\nessa liderança melhora a vida de todos aqueles que mais amo, pois \\no contexto no qual e onde eu vivo é o mesmo no qual você vive \\ne, assim, logo vejo que o seu querer viver é semelhante ao meu.   \\nComo já expliquei, os meus desejos e as minhas i ntenções \\nestão atrelados à ideia de querer agregar para o seu viver melhor.  \\nVejo, desse modo, que é necessário para o meu viver melhor o \\nseu viver melhor, isso me faz escrever algo que possa nos ajuda ra \\nchegar perto do impossível, ou seja, um viver bem c om todos.",
      "position": 1577,
      "chapter": 1,
      "page": 3,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 35.08274336283186,
      "complexity_metrics": {
        "word_count": 226,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.666666666666664,
        "avg_word_length": 4.442477876106195,
        "unique_word_ratio": 0.6371681415929203,
        "avg_paragraph_length": 226.0,
        "punctuation_density": 0.11061946902654868,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "vejo",
          "melhor",
          "qual",
          "querer",
          "saber",
          "essa",
          "assim",
          "trabalho",
          "presidente",
          "impossível",
          "logo",
          "algo",
          "possa",
          "muito",
          "mesmo",
          "como",
          "pois",
          "grandeza",
          "tenho"
        ],
        "entities": [
          [
            "Logo",
            "PERSON"
          ],
          [
            "eu vejo",
            "PERSON"
          ],
          [
            "sendo muito prepotente",
            "PERSON"
          ],
          [
            "mesmo arrogante em querer direcionar",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "vejo não saber",
            "ORG"
          ],
          [
            "consciência de que",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "melhora",
            "GPE"
          ]
        ],
        "readability_score": 79.83392330383481,
        "semantic_density": 0,
        "word_count": 226,
        "unique_words": 144,
        "lexical_diversity": 0.6371681415929203
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "Capítulo 1  \\nQuantos tipos de pessoas temos e como elas  adquirem o seu \\nviver?    \\nTodos os estados têm um costume de viver de acordo com \\na sua própria evolução territorial, o estado que cria uma \\nsemelhança em um viver comum entre todos aqueles que ali \\nvivem é o mesmo que gera diferença entre o próprio povo, \\nfazendo, assim, termos difere nças de pensamentos nas cidades, \\nbairros e até mesmo pequenos territórios.    \\nDevido a esses acontecimentos e a ganância do próprio \\nhomem, transformamo -nos em pessoas de objetivos semelhantes, \\npois vivemos no mesmo país, mas com cultura diferente de estado \\npara estado, bairros dentro do próprio estado com objetivos de \\nviver diferentes um do outro e, para finalizar, as dificuldades de \\ncomo cada um adquire o seu próprio viver vêm das suas próprias \\ndores, estrutura familiar, local onde vive, como vive, como \\nenxerga e como interpreta a vida.   \\nIsso tudo sem falar da ganância do humano, o qual não \\nsabe viver entre si e respeitar, assim, logo venho te dizer que \\npoucos são afortunados em ter sabedoria para viver, pois a vida,",
      "position": 2968,
      "chapter": 1,
      "page": 4,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.453591160220995,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 45.25,
        "avg_word_length": 4.845303867403315,
        "unique_word_ratio": 0.6685082872928176,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.1270718232044199,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "como",
          "estado",
          "próprio",
          "entre",
          "mesmo",
          "pessoas",
          "todos",
          "assim",
          "bairros",
          "ganância",
          "objetivos",
          "pois",
          "vive",
          "vida",
          "capítulo",
          "quantos",
          "tipos",
          "temos",
          "elas"
        ],
        "entities": [
          [
            "Todos",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "próprio povo",
            "GPE"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "cultura diferente de estado \\npara estado",
            "PERSON"
          ],
          [
            "para finalizar",
            "PERSON"
          ],
          [
            "dizer que \\npoucos são",
            "ORG"
          ]
        ],
        "readability_score": 75.921408839779,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 121,
        "lexical_diversity": 0.6685082872928176
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "muitas vezes, é tão cruel que a maior l iderança que alguns \\nenxergam é direcionada àqueles que pagam comida, fazem \\nchurrasco e pagam cerveja. Esses mesmos que se curvam a esse \\ntipo de suborno são os mesmos que só trabalham para sobreviver, \\no mesmo “estilo de vida” que o faz ter poucos momentos d e \\nfelicidade o faz ser facilmente subornado  devido a própria \\nmiséria.",
      "position": 4197,
      "chapter": 1,
      "page": 5,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.643846153846155,
      "complexity_metrics": {
        "word_count": 65,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 32.5,
        "avg_word_length": 4.6461538461538465,
        "unique_word_ratio": 0.7692307692307693,
        "avg_paragraph_length": 65.0,
        "punctuation_density": 0.07692307692307693,
        "line_break_count": 6,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pagam",
          "mesmos",
          "muitas",
          "vezes",
          "cruel",
          "maior",
          "iderança",
          "alguns",
          "enxergam",
          "direcionada",
          "àqueles",
          "comida",
          "fazem",
          "churrasco",
          "cerveja",
          "esses",
          "curvam",
          "esse",
          "tipo",
          "suborno"
        ],
        "entities": [
          [
            "l iderança",
            "NORP"
          ],
          [
            "direcionada àqueles",
            "PERSON"
          ],
          [
            "mesmos que",
            "PERSON"
          ],
          [
            "mesmos que",
            "PERSON"
          ],
          [
            "só trabalham",
            "PERSON"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 82.35615384615384,
        "semantic_density": 0,
        "word_count": 65,
        "unique_words": 50,
        "lexical_diversity": 0.7692307692307693
      },
      "preservation_score": 1.5810445081318458e-06
    },
    {
      "id": 1,
      "text": "Capítulo 2   \\n“A herança do sentimento humano”   \\n           Aqui eu digo: o líder que conquistou a liderança através da \\nsua própria vida foi devido à semelhança de caráter entre aqueles \\nque ele li dera.   \\nDevido a esse pensamento dito logo acima, ressalto que \\nconhecer quem um líder pode confiar é ampliar o seu caráter para \\noutros que irão confiar na sua liderança, essa mesma liderança \\nque vem com sentimentos que pesam em você ser um melhor líder \\né o mesmo sentimento que ocasiona a falta de reconhecimento do \\nseu próprio caráter que o fez ser líder.   \\nA falta do caráter de um líder perante a sua própria \\nliderança ocasiona perda de confiança daqueles que o seguiam, se \\nisso acontece devido a um caráter, como um herdeiro de uma \\nliderança irá prosseguir sem ser de caráter semelhante àqueles que \\no antecessor liderava?   \\nAssim, nós deixamos em aberto todos os tipos de \\nsentimentos humanos, de como possa ser feito um líder digno \\ndiante da sua própria conquista,  pois ele teve um trajeto cheios de",
      "position": 4706,
      "chapter": 2,
      "page": 6,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.41754385964912,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 42.75,
        "avg_word_length": 4.7251461988304095,
        "unique_word_ratio": 0.6198830409356725,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.06432748538011696,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "caráter",
          "liderança",
          "própria",
          "devido",
          "sentimento",
          "confiar",
          "sentimentos",
          "ocasiona",
          "falta",
          "como",
          "capítulo",
          "herança",
          "humano",
          "aqui",
          "digo",
          "conquistou",
          "através",
          "vida",
          "semelhança"
        ],
        "entities": [
          [
            "2",
            "CARDINAL"
          ],
          [
            "Aqui eu",
            "PERSON"
          ],
          [
            "semelhança de caráter",
            "ORG"
          ],
          [
            "que ele li",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para \\noutros",
            "PERSON"
          ],
          [
            "irão",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "ocasiona",
            "GPE"
          ]
        ],
        "readability_score": 77.20745614035087,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 106,
        "lexical_diversity": 0.6198830409356725
      },
      "preservation_score": 8.808676545305998e-06
    },
    {
      "id": 1,
      "text": "“gostosuras ou travessuras”. Então, como absorver e assimilar \\ntodo esse trajeto necessário para ser um líder?",
      "position": 5882,
      "chapter": 1,
      "page": 7,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.7625,
      "complexity_metrics": {
        "word_count": 16,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 5.875,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.1875,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "gostosuras",
          "travessuras",
          "então",
          "como",
          "absorver",
          "assimilar",
          "todo",
          "esse",
          "trajeto",
          "necessário",
          "líder"
        ],
        "entities": [
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 94.2375,
        "semantic_density": 0,
        "word_count": 16,
        "unique_words": 16,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.8821958430141024e-07
    },
    {
      "id": 1,
      "text": "Capítulo 3   \\nA variedade humana   \\n         A variedade de diferença comportamental é a primeira \\ndificuldade que um líder encontra, pois os mesmos liderados, ao \\ncombinar um salário, por exemplo, muitas vezes esse mesmo \\nsalário não será satisfatório, isso ocorre por vários fatores \\ncomportamentais hum anos.   \\nVamos pensar em uma linha de raciocínio que investigue \\na criação de caráter da pessoa. Esse caráter construído vem de \\numa origem, qual foi essa origem? Como foi o trajeto? Como foi \\na absorção de direcionamento? Teve direcionamento? Essas são \\nalguma s das reflexões necessárias.    \\nPensa comigo: o que você quer para o seu filho? Muitas \\npessoas respondem que querem que seus filhos sejam médicos, \\nempresários, advogados e todas aquelas profissões que aparentam \\nser mais dignas do que um lavador de carro, p olidor, instalador de \\nInsulfilm.   \\n“Assim é a mente humana, pois aqueles mesmos que um \\ndia estavam na miséria sabem  \\nque a miséria não é boa de se viver.”",
      "position": 6157,
      "chapter": 3,
      "page": 8,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.62574780058651,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 14.090909090909092,
        "avg_word_length": 5.116129032258065,
        "unique_word_ratio": 0.7483870967741936,
        "avg_paragraph_length": 155.0,
        "punctuation_density": 0.14193548387096774,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "variedade",
          "humana",
          "pois",
          "mesmos",
          "salário",
          "muitas",
          "esse",
          "caráter",
          "origem",
          "como",
          "direcionamento",
          "miséria",
          "capítulo",
          "diferença",
          "comportamental",
          "primeira",
          "dificuldade",
          "líder",
          "encontra",
          "liderados"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "construído vem de \\numa origem",
            "PERSON"
          ],
          [
            "alguma s",
            "PERSON"
          ],
          [
            "Pensa",
            "PERSON"
          ],
          [
            "para o",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "querem que",
            "PERSON"
          ],
          [
            "médicos",
            "PRODUCT"
          ]
        ],
        "readability_score": 91.41970674486804,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 116,
        "lexical_diversity": 0.7483870967741936
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "Assim, ocorre o sentimento de nunca estarmos satisfeitos \\ncom aquilo que estamos vivendo, pois sempr e queremos ser mais \\ne ter mais, o que faz com que tenhamos poucos profissionais \\ncapacitados, pois muitos pensam que o melhor é pular de galho \\nem galho, em vez de querer melhorar aquilo que estão vivendo \\ncom insatisfação.    \\n“Essa insatisfação, por sua vez, cria guerra que gera guerra \\na qual não consegue permanecer.”   \\nDependendo de onde você está liderando e a quem está \\nliderando ocorrem formas diferentes de se manter ou até mesmo \\nse criar um vínculo de confiança, pois lembre -se: aquele líder que \\nconquistou a confiança através do caráter, a semelhança no trajeto \\no faz entender o quão fraco nós somos. Se um humano chegou a \\nser líder sabe o quão difícil é estar nessa posição e, além disso, \\ncabe ressaltar que poucos são beneficia dos do dom de ser líder, \\nmesmo quem tem o dom de ser líder tem as fraquezas dos \\nliderados. São os mesmos que, quando têm uma fartura na vida, \\nmuitas vezes, não sabem controlar os próprios impulsos, pois \\nviver fora da miséria que já estão acostumados é a ma ior \\nfelicidade que eles podem ter...",
      "position": 7303,
      "chapter": 1,
      "page": 9,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.307575757575755,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 39.6,
        "avg_word_length": 4.691919191919192,
        "unique_word_ratio": 0.696969696969697,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.12121212121212122,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "líder",
          "aquilo",
          "vivendo",
          "mais",
          "poucos",
          "galho",
          "estão",
          "insatisfação",
          "guerra",
          "está",
          "liderando",
          "quem",
          "mesmo",
          "confiança",
          "quão",
          "assim",
          "ocorre",
          "sentimento",
          "nunca"
        ],
        "entities": [
          [
            "sentimento de nunca estarmos",
            "ORG"
          ],
          [
            "que estamos vivendo",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "vez de querer melhorar",
            "PERSON"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "por sua vez",
            "ORG"
          ],
          [
            "cria guerra",
            "ORG"
          ],
          [
            "Dependendo de",
            "ORG"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 78.79242424242425,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 138,
        "lexical_diversity": 0.696969696969697
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "Como podemos manter o vínculo daqueles que contemplaram a \\nminha miséria?   \\nTirando -os da miséria que você viveu.   \\nPorém, para se fazer isso, teríamos que nos privar de \\ncertos luxos, teríamos que nos privar de termos um carro melhor, \\numa casa melhor, uma comida melhor e, devido a esse \\n“sacrifício”, nós teríamos que controlar os nossos instintos \\nprimitivos, aqueles que, quando se têm ausência, fazem -nos \\nperder o controle de nós mesmos.   \\nPor isso, trabalhar com miseráve is facilita a felicidade da \\nprópria ganância de um líder, pois eles se satisfazem com a \\npobreza. A pobreza se torna luxo para a miséria, torna -se luxo \\npara a ganância, mas lembre -se: os mesmos miseráveis não \\ncontrolam os seus próprios impulsos, o que faz c om que um líder \\nse torne sem liderança perante a confiança, e sim um líder pela \\nganância.   \\nA ausência de reconhecer os liderados e de perceber a sua \\nprópria ganância faz alguns líderes pensarem que a miséria é a \\nfacilidade em controlar a minha evolução, p orém esse mesmo \\npensamento o faz ficar cego diante daqueles que são miseráveis",
      "position": 8571,
      "chapter": 1,
      "page": 10,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.692622950819672,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.5,
        "avg_word_length": 4.808743169398907,
        "unique_word_ratio": 0.6557377049180327,
        "avg_paragraph_length": 183.0,
        "punctuation_density": 0.12568306010928962,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miséria",
          "ganância",
          "teríamos",
          "melhor",
          "líder",
          "daqueles",
          "minha",
          "isso",
          "privar",
          "esse",
          "controlar",
          "ausência",
          "mesmos",
          "própria",
          "pobreza",
          "torna",
          "luxo",
          "miseráveis",
          "como",
          "podemos"
        ],
        "entities": [
          [
            "vínculo daqueles",
            "PERSON"
          ],
          [
            "Tirando -os da miséria",
            "ORG"
          ],
          [
            "Porém",
            "PERSON"
          ],
          [
            "fazer",
            "ORG"
          ],
          [
            "teríamos",
            "PERSON"
          ],
          [
            "uma comida melhor e",
            "ORG"
          ],
          [
            "nós teríamos",
            "ORG"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "têm ausência",
            "ORG"
          ],
          [
            "controle de nós mesmos",
            "ORG"
          ]
        ],
        "readability_score": 83.30737704918033,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 120,
        "lexical_diversity": 0.6557377049180327
      },
      "preservation_score": 2.0741798190015406e-05
    },
    {
      "id": 1,
      "text": "evoluídos. Esses miseráveis não observados são os mesmos que \\npodem fazer um líder voltar a estar no local do miserável e, de \\noutro modo, o miserável evoluído se transformar em u m líder. \\nAssim como na selva os leões mais fortes ficam com as fêmeas, \\ncomem a melhor parte da comida, na vida real muitos têm \\nganância pelo mesmo motivo que o nosso.   \\nLogo, não pense que estar na liderança o faz ser melhor, \\nser mais, ter mais, pois se o líder pensar assim, a ruína devido à \\nsua própria ganância o faz ser arruinado na vida, não pelo \\ndinheiro, e sim pelo sentimento de estar feliz com aqueles que te \\nfazem feliz.   \\nVoltaremos ao assunto de ser exemplo para aqueles que o \\nlíder lidera, até porqu e esse mesmo exemplo é a razão de ser \\nseguido, aqueles que o seguem o admiram por qual motivo? Esse \\nmotivo que foi gerado não se pode faltar quando é necessário, pois \\nseja através da ganância, seja através da confiança, ambos têm o \\nmesmo valor de tamanho  \\nproporcional à liderança. Logo, “isso expõe que a falta de \\nrecursos faz o humano ser doutrinado por aquele que tem mais",
      "position": 9776,
      "chapter": 1,
      "page": 11,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 30.262417582417584,
      "complexity_metrics": {
        "word_count": 195,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.857142857142858,
        "avg_word_length": 4.446153846153846,
        "unique_word_ratio": 0.6410256410256411,
        "avg_paragraph_length": 195.0,
        "punctuation_density": 0.11794871794871795,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "mais",
          "ganância",
          "pelo",
          "mesmo",
          "motivo",
          "aqueles",
          "miserável",
          "assim",
          "melhor",
          "vida",
          "logo",
          "liderança",
          "pois",
          "feliz",
          "exemplo",
          "esse",
          "seja",
          "através",
          "evoluídos"
        ],
        "entities": [
          [
            "mesmos",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "ganância pelo mesmo",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "faz ser melhor",
            "ORG"
          ],
          [
            "própria ganância",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "não pelo \\ndinheiro",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "de estar",
            "PERSON"
          ]
        ],
        "readability_score": 84.73758241758242,
        "semantic_density": 0,
        "word_count": 195,
        "unique_words": 125,
        "lexical_diversity": 0.6410256410256411
      },
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "id": 1,
      "text": "recursos”, pois esse aspecto faz com que alguns sejam dignos de \\nserem seguidos.   \\nAssim, percebe -se o quanto o humano é uma espécie \\ndoen te no que se refere à ganância, pois sempre precisa estar em \\nguerra. Sendo assim, ocorre a necessidade de ser enjaulado na \\nprópria felicidade, pois ninguém iria seguir um líder que não \\ndemostra confiança pelo trajeto, e sim pela ganância.   \\nQuando não se e nxerga os erros de uma liderança no \\ninício, há a ausência de enxergar os erros futuros, pois problemas \\nnão são evitados, mas apenas adiados em benefício dos outros. \\nAssim, o quanto antes forem descobertas as falhas na liderança, \\nmelhor será a liderança, po is prevenir a falha é conquistar a \\ntranquilidade para pensar e melhorar a própria liderança.   \\nQuando não se enxerga as falhas é o início da falta de \\ncontrole pelo seu próprio desejo, pois esse aspecto torna o líder \\ncego, fazendo com que guerras desnecessá rias que poderiam \\nter  sido  controladas  sejam  \\ndesenvolvidas e isso ocorre “devido a se perder entre o bem em \\nmal e o mal em bem”. Essa falta de percepção o faz imaginar que \\né mais forte do que pensa e nem sempre nós somos tão fortes",
      "position": 10976,
      "chapter": 1,
      "page": 12,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 30.751172707889125,
      "complexity_metrics": {
        "word_count": 201,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.714285714285715,
        "avg_word_length": 4.646766169154229,
        "unique_word_ratio": 0.6616915422885572,
        "avg_paragraph_length": 201.0,
        "punctuation_density": 0.09950248756218906,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "liderança",
          "assim",
          "esse",
          "aspecto",
          "sejam",
          "quanto",
          "ganância",
          "sempre",
          "ocorre",
          "própria",
          "líder",
          "pelo",
          "quando",
          "erros",
          "início",
          "falhas",
          "falta",
          "recursos",
          "alguns"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "Assim",
            "GPE"
          ],
          [
            "precisa estar",
            "PERSON"
          ],
          [
            "Sendo",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "erros de uma",
            "ORG"
          ],
          [
            "ausência de enxergar os",
            "ORG"
          ],
          [
            "mas apenas",
            "PERSON"
          ],
          [
            "Assim",
            "GPE"
          ]
        ],
        "readability_score": 84.24882729211087,
        "semantic_density": 0,
        "word_count": 201,
        "unique_words": 133,
        "lexical_diversity": 0.6616915422885572
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "quanto parecemos, e ssa falta de reconhecer nossa própria falha \\nnos faz imaginar que somos mais do que imaginávamos. No \\ntrajeto de ser líder, o comum desejo da conquista é a conquista da \\nconfiança em ser líder, assim o líder sempre é louvado e não \\ncensurado, pois o mesmo traj eto que o fez ser líder o fez ser \\nadmirado e ser admirado sempre o fez perder se  nas próprias \\nfalhas devido às vezes que não foi capaz de reconhecê -las pela \\nprópria liderança que o deixava cego pela luxúria vívida.      \\nTudo o que foi falado neste capítulo  nos mostra o quanto \\num líder precisa dos liderados. Os mesmos liderados que fazem a \\nliderança ganhar a guerra através da ganância são os mesmos que \\nfazem perder através da ganância, assim como também foi dito \\nque se pode ganhar a liderança através da conf iança do mesmo \\nmodo que é possível perdê -la.",
      "position": 12255,
      "chapter": 1,
      "page": 13,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.30921052631579,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 38.0,
        "avg_word_length": 4.473684210526316,
        "unique_word_ratio": 0.5986842105263158,
        "avg_paragraph_length": 152.0,
        "punctuation_density": 0.05921052631578947,
        "line_break_count": 13,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "liderança",
          "através",
          "quanto",
          "própria",
          "conquista",
          "assim",
          "sempre",
          "mesmo",
          "admirado",
          "perder",
          "pela",
          "liderados",
          "mesmos",
          "fazem",
          "ganhar",
          "ganância",
          "parecemos",
          "falta",
          "reconhecer"
        ],
        "entities": [
          [
            "quanto parecemos",
            "PERSON"
          ],
          [
            "ssa falta de reconhecer",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "que somos mais",
            "PERSON"
          ],
          [
            "louvado",
            "PERSON"
          ],
          [
            "deixava cego pela luxúria vívida",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "mostra",
            "LOC"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 79.65789473684211,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 91,
        "lexical_diversity": 0.5986842105263158
      },
      "preservation_score": 5.383080111020332e-06
    },
    {
      "id": 1,
      "text": "Capítulo 4   \\n \\nComo manter os novos liderados?   \\n  Conforme o tamanho da liderança vai aumentando, a quantidade \\nde liderados também necessita de atenção. Esses novos liderados \\nprecisam de tempo e investimento, pois os que já estão sendo \\nliderados, como dito no capítulo anterior, precisam evoluir junto \\nao líder. Sendo assim, os novos liderados, quando assumem um \\nlocal de maior importância, não pela confiança, e sim pela \\nnecessidade da sua especialização no que se refere à mão de obra, \\nlogo esse mesmo liderado que veio através de uma necessidade \\npode se torna r um incômodo ou uma evolução fora da curva. \\nAssim, esse mesmo que inicialmente vem para agregar pode ser \\nesse mesmo que possa vir para destruir, assim como o trajeto do \\nlíder é exemplo para aqueles liderados, o papel desse novo \\nliderado por muitas vezes s e torna mais importante do que aquele \\nque é o seu braço direito. Isso pode causar um mal -estar para \\naqueles liderados que se achavam aptos a fazer determinada \\nfunção. Nesse contexto, o líder automaticamente terá a \\nnecessidade de construir novos cargos de l ideranças secundárias. \\nÉ necessário, então, estimular o seguinte questionamento: esses",
      "position": 13278,
      "chapter": 4,
      "page": 14,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.40342105263158,
      "complexity_metrics": {
        "word_count": 190,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.75,
        "avg_word_length": 5.094736842105263,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 190.0,
        "punctuation_density": 0.12105263157894737,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liderados",
          "novos",
          "como",
          "líder",
          "assim",
          "necessidade",
          "esse",
          "mesmo",
          "pode",
          "capítulo",
          "esses",
          "precisam",
          "sendo",
          "pela",
          "liderado",
          "torna",
          "aqueles",
          "manter",
          "conforme",
          "tamanho"
        ],
        "entities": [
          [
            "Como",
            "ORG"
          ],
          [
            "Conforme",
            "NORP"
          ],
          [
            "já estão",
            "PERSON"
          ],
          [
            "precisam evoluir junto",
            "ORG"
          ],
          [
            "Sendo",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "veio através de uma",
            "PERSON"
          ],
          [
            "para destruir",
            "PERSON"
          ],
          [
            "torna mais importante",
            "PERSON"
          ]
        ],
        "readability_score": 86.59657894736841,
        "semantic_density": 0,
        "word_count": 190,
        "unique_words": 130,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 1.8069080092935382e-05
    },
    {
      "id": 1,
      "text": "líderes secundários têm que ser aqueles que têm uma maior \\nconfiança de todos ou aqueles que têm a maior confiança do líder?   \\n “A falsa divisão do poder é o controle par a quem tem mais \\npoder.”    \\nTodos os líderes que exerceram grandes lideranças ou que \\nexercem grandes lideranças têm líderes secundários de confiança \\nao seu lado, logo isso nos faz perceber que a necessidade de \\nlíderes secundários depende de como a liderança  foi conquistada. \\nSe esse processo ocorreu através da ganância pela ganância, ela \\nmantém um líder secundário bom em desenvolvimento.  Por outro \\nlado, para se manter a liderança precisa -se de um líder secundário \\nde confiança em qualquer contexto.   \\n“Ter pod er sobre quem tem poder é o controle hereditário dos \\nfuturos líderes.”   \\nAmbos os lados, caráter ou ganância, precisam de líderes \\nsecundários à altura da liderança secundária proporcional ao \\nquerer evoluir do líder, pois caso o líder evolua fará os outros \\nevoluírem também. Assim, se um líder evolui todos os liderados \\nirão evoluir de forma proporcional a ele, até porque todos os \\nliderados só fazem aquilo que o líder “permite fazer” para se",
      "position": 14617,
      "chapter": 1,
      "page": 15,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.197229729729727,
      "complexity_metrics": {
        "word_count": 185,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.125,
        "avg_word_length": 5.032432432432432,
        "unique_word_ratio": 0.6054054054054054,
        "avg_paragraph_length": 185.0,
        "punctuation_density": 0.08108108108108109,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "líderes",
          "secundários",
          "confiança",
          "todos",
          "poder",
          "liderança",
          "ganância",
          "aqueles",
          "maior",
          "controle",
          "quem",
          "grandes",
          "lideranças",
          "lado",
          "secundário",
          "proporcional",
          "evoluir",
          "liderados",
          "falsa"
        ],
        "entities": [
          [
            "que",
            "CARDINAL"
          ],
          [
            "Todos",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "perceber",
            "PRODUCT"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "da ganância pela ganância",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "para se manter",
            "PERSON"
          ],
          [
            "Ambos",
            "PERSON"
          ]
        ],
        "readability_score": 86.92777027027027,
        "semantic_density": 0,
        "word_count": 185,
        "unique_words": 112,
        "lexical_diversity": 0.6054054054054054
      },
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "id": 1,
      "text": "manter  no controle de ser um bom líder. Consequentemente, \\nquando esse s liderados evoluem, logo podem querer ser líderes \\nde si mesmos, afetando toda a engrenagem a qual o líder liderava, \\npois logo que se perde esse futuro líder perde -se uma peça \\nfundamental na sua liderança; não sabendo o motivo da perda \\ndesse líder secundár io se é devido à falta de recursos, ganância, \\ncontexto dos liderados ou até mesmo vontade própria de evoluir, \\npois o mesmo líder que o fez ser grande é o mesmo líder exemplo \\nque o fez crescer. Logo, o líder secundário enxerga a necessidade \\nde evoluir mais que o contexto no qual está inserido, pois se \\ncontinuar no mesmo espaço não irá chegar ao tamanho da \\nevolução e da liderança que pode atingir.   \\n“A falta de recursos nos torna escravos da própria escassez, \\ntornando -nos fáceis  \\nsubordinados.”   \\n Esse  novo  líder  torna -se  um  \\n“incômodo” para o antigo líder, pois esse mesmo líder novo saiu \\nde uma antiga liderança que tinha falhas e que ocasionou \\nincômodos para os “miseráveis” insatisfeitos com a sua posição. \\nLogo, esses miseráveis conseguem ating ir uma grande",
      "position": 15879,
      "chapter": 1,
      "page": 16,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.116934046345804,
      "complexity_metrics": {
        "word_count": 187,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 31.166666666666668,
        "avg_word_length": 4.834224598930481,
        "unique_word_ratio": 0.6256684491978609,
        "avg_paragraph_length": 187.0,
        "punctuation_density": 0.0962566844919786,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "mesmo",
          "esse",
          "logo",
          "pois",
          "liderança",
          "liderados",
          "qual",
          "perde",
          "falta",
          "recursos",
          "contexto",
          "própria",
          "evoluir",
          "grande",
          "torna",
          "novo",
          "miseráveis",
          "manter",
          "controle"
        ],
        "entities": [
          [
            "manter",
            "PERSON"
          ],
          [
            "Consequentemente",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "querer ser",
            "PERSON"
          ],
          [
            "liderava",
            "PERSON"
          ],
          [
            "não sabendo",
            "GPE"
          ],
          [
            "da perda",
            "PERSON"
          ],
          [
            "própria de evoluir",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ]
        ],
        "readability_score": 82.96639928698752,
        "semantic_density": 0,
        "word_count": 187,
        "unique_words": 117,
        "lexical_diversity": 0.6256684491978609
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "oportunidade de serem melhores miseráveis. Assim, o antigo líder \\nse sente incomodado pelo novo líder, pois o antigo líder não \\nentende o motivo e, se entende, tem dificuldade  para  aceitar a \\nperda dos miseráveis instruídos, pois eles tiveram investimentos \\npara exercer um melhor trabalho para o líder antigo. Logo, aquele \\nlíder secundário amado pelo líder antigo sente incômodo, não por \\nter culpa, e sim pelo antigo líder ficar decepcionado com o novo \\nlíder.   \\nO novo miserável de um novo líder log o enxerga que a \\nmiséria ao lado do novo líder é menos miserável que ao lado do \\nantigo, pois lá onde estava era obrigado a fazer o seu trabalho. No \\ncontexto novo, pode se limitar a fazer a sua própria vontade, \\ntornando -se um miserável estável. Todos aqueles  que se \\nencontram na miséria não querem permanecer, assim tornamse \\npresas fáceis para outros líderes, pois esses mesmos miseráveis \\nsão mais fáceis de serem conquistados não pela ganância, e sim \\npor uma necessidade básica de viver melhor. No entanto, só o \\npoder material não é o suficiente para controlar o poder do \\nmiserável inteligente, pois percebe que há mediocridade na \\nmiséria, já que ali há muito  mais miséria do  que a miséria a qual \\nele merecia estar.",
      "position": 17116,
      "chapter": 1,
      "page": 17,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.17787794729542,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.428571428571427,
        "avg_word_length": 4.878640776699029,
        "unique_word_ratio": 0.6067961165048543,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.11650485436893204,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "antigo",
          "novo",
          "pois",
          "miséria",
          "miserável",
          "miseráveis",
          "pelo",
          "serem",
          "assim",
          "sente",
          "entende",
          "melhor",
          "trabalho",
          "lado",
          "fazer",
          "fáceis",
          "mais",
          "poder",
          "oportunidade"
        ],
        "entities": [
          [
            "oportunidade de serem melhores miseráveis",
            "PERSON"
          ],
          [
            "sente",
            "ORG"
          ],
          [
            "pelo novo",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "antigo sente incômodo",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "novo miserável de um novo",
            "PERSON"
          ],
          [
            "log o",
            "ORG"
          ],
          [
            "novo líder",
            "PERSON"
          ],
          [
            "miséria não querem",
            "PERSON"
          ]
        ],
        "readability_score": 83.82212205270457,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 125,
        "lexical_diversity": 0.6067961165048543
      },
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "id": 1,
      "text": "Assim, isso me faz pensar:   \\nQual é o valor mone tário da necessidade de viver de um \\nmiserável?   \\nQual é o valor da conquista para se viver bem?   \\nQual é o sentimento que temos que seguir?   \\nQuais são os valores sentimentais ou materiais?    \\nO sentimento de conquista de um miserável para outro \\nvaria muit o, essa variação vem de ter muito dinheiro a quase não \\nter dinheiro, existe uma diferença de vida de quem ganha 200 mil \\npor mês e gasta R$ 220 mil por mês, ou seja, está vivendo um   \\n“perrengue chique”, pois o sentimento de viver em liberdade é \\nmenor do qu e a liberdade de quem vive ganhando R$ 3 mil e se \\nadapta a esses recursos. Além disso, esses sujeitos podem se \\ndivertir com menos peso do que os líderes que têm pessoas que \\nos veem como “exemplo” e precisam dele para sobreviver.   \\n“Há líderes miseráveis e há mendigos ricos, ambos os lados \\ndependem do estado  \\nsentimental de como é viver para cada um.”",
      "position": 18472,
      "chapter": 1,
      "page": 18,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.869642857142857,
      "complexity_metrics": {
        "word_count": 168,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 21.0,
        "avg_word_length": 4.357142857142857,
        "unique_word_ratio": 0.6488095238095238,
        "avg_paragraph_length": 168.0,
        "punctuation_density": 0.09523809523809523,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "qual",
          "sentimento",
          "valor",
          "miserável",
          "conquista",
          "dinheiro",
          "quem",
          "liberdade",
          "esses",
          "líderes",
          "como",
          "assim",
          "isso",
          "pensar",
          "mone",
          "tário",
          "necessidade",
          "temos",
          "seguir"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "Quais",
            "GPE"
          ],
          [
            "para outro",
            "PERSON"
          ],
          [
            "essa variação vem de",
            "ORG"
          ],
          [
            "muito dinheiro",
            "PERSON"
          ],
          [
            "diferença de vida de quem",
            "ORG"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "220",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "sobreviver",
            "GPE"
          ]
        ],
        "readability_score": 88.19285714285715,
        "semantic_density": 0,
        "word_count": 168,
        "unique_words": 109,
        "lexical_diversity": 0.6488095238095238
      },
      "preservation_score": 1.4078824905745484e-05
    },
    {
      "id": 1,
      "text": "Não há como deixar de pensar sobre o padrão \\ncomportamental territorial, o que me faz pensar que os líderes que \\nmais têm seguidores são aqueles que mais se as semelham com a \\nforma de liderança. Assim, isso mostra que o caminho de \\naceitação de um para com o outro representa a necessidade de um \\nviver melhor de um para com todos, pois já vivemos a ideia de \\npadronizar as histórias religiosas em geral, impérios, mona rquia, \\nfilosofias e muitas outras tentativas de direcionamentos em que \\napenas um direcionamento passa ser a forma de viver \\ncorretamente. Logo, sua forma é um erro de viver a sua própria \\nvida sem ver e respeitar o viver do outro, uma vez que não \\nviveram uma  vida de caos semelhante à do outro, por isso julgam \\na forma de ver a vida do outro sem argumentar, e sim ter certeza.   \\nPara finalizar este capítulo, é necessário destacar que “ um \\nlíder com uma liderança com grande network pode mover \\nmontanhas, isso nos faz perceber a diferença de um grande líder \\npara líderes secundários, pois o grande líder consegue ter a \\nsabedoria de vários miseráveis, não por ser inteligente, e sim por \\nter sab edoria pelo sentimento do semelhante.”  Capítulo 5",
      "position": 19522,
      "chapter": 5,
      "page": 19,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.78048780487805,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 41.0,
        "avg_word_length": 4.634146341463414,
        "unique_word_ratio": 0.5756097560975609,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.09268292682926829,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "outro",
          "viver",
          "isso",
          "vida",
          "líder",
          "grande",
          "pensar",
          "líderes",
          "mais",
          "liderança",
          "pois",
          "semelhante",
          "capítulo",
          "como",
          "deixar",
          "padrão",
          "comportamental",
          "territorial",
          "seguidores"
        ],
        "entities": [
          [
            "deixar de pensar",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "semelham",
            "ORG"
          ],
          [
            "mostra que",
            "NORP"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "já vivemos",
            "PERSON"
          ],
          [
            "impérios",
            "GPE"
          ],
          [
            "mona",
            "GPE"
          ],
          [
            "tentativas",
            "CARDINAL"
          ],
          [
            "Logo",
            "PERSON"
          ]
        ],
        "readability_score": 78.10975609756098,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 118,
        "lexical_diversity": 0.5756097560975609
      },
      "preservation_score": 1.4229400573186614e-05
    },
    {
      "id": 1,
      "text": "Como governar os estados e as cidades que têm várias  \\nreligiões, milícias, tráfico e aquelas que vivem com as \\npróprias leis.   \\n  Como foi dito, quando os miseráveis se acostumam com a \\nmiséria, viver ent re a miséria é confortável, pois ali se tem \\nliberdade entre os semelhantes de viver em caos sentimental, \\nmonetário e territorial e isso nos faz criar sentimentos de tanto \\namor que criamos ódio quando não temos aqueles semelhantes ao \\nlado, pois para viver e m felicidade na religião, junto a lugares em \\nque se tem guerra, tráfico e milícias, por exemplo, é necessário \\nter muito ódio e amor, até porque nenhum miserável quer ser \\nmiserável. Porém, aquela semelhança com a miséria nos faz \\nencontrar muito “amor  \\nplatô nico” na miséria, pois a única coisa que sobra que nos faz \\nfeliz na miséria é a mais bela forma de ser feliz, a mesma que nos \\ndá força, confiança, segurança e todas as formas de amar. Quem \\njá passou fome sabe o quão difícil é viver com a vergonha de \\npassar  fome, não só por passar fome, e sim por toda a situação \\ndevido ao território de onde a miséria vive. Lugares onde não se \\npode ter grandes líderes pela escassez de recursos e ainda existe \\no julgamento de ser visto pela forma de vida a qual ninguém",
      "position": 20816,
      "chapter": 1,
      "page": 20,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.356818181818184,
      "complexity_metrics": {
        "word_count": 220,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 44.0,
        "avg_word_length": 4.5227272727272725,
        "unique_word_ratio": 0.6136363636363636,
        "avg_paragraph_length": 220.0,
        "punctuation_density": 0.10454545454545454,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miséria",
          "viver",
          "pois",
          "amor",
          "fome",
          "como",
          "milícias",
          "tráfico",
          "quando",
          "semelhantes",
          "ódio",
          "lugares",
          "muito",
          "miserável",
          "feliz",
          "forma",
          "passar",
          "onde",
          "pela",
          "governar"
        ],
        "entities": [
          [
            "Como",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "ali se",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "quando não temos",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Porém",
            "ORG"
          ],
          [
            "aquela semelhança",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 76.64318181818182,
        "semantic_density": 0,
        "word_count": 220,
        "unique_words": 135,
        "lexical_diversity": 0.6136363636363636
      },
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "id": 1,
      "text": "escolheu , apenas foi inserido ao nascer, simplesmente nasceu na \\nmiséria sem culpa, sendo culpado por algo que nem cometeu \\nantes mesmo de cometer, por muitas vezes cometendo atos pela \\nnecessidade de sobrevivência e por muitas outras para ser um \\nlíder. No entanto, e sses que chegaram na liderança dessa forma \\nsão os mesmos que cometeram grandes atrocidades religiosas e \\ngananciosas.",
      "position": 22173,
      "chapter": 1,
      "page": 21,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.83360655737705,
      "complexity_metrics": {
        "word_count": 61,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 30.5,
        "avg_word_length": 5.278688524590164,
        "unique_word_ratio": 0.8524590163934426,
        "avg_paragraph_length": 61.0,
        "punctuation_density": 0.11475409836065574,
        "line_break_count": 6,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "muitas",
          "escolheu",
          "apenas",
          "inserido",
          "nascer",
          "simplesmente",
          "nasceu",
          "miséria",
          "culpa",
          "sendo",
          "culpado",
          "algo",
          "cometeu",
          "antes",
          "mesmo",
          "cometer",
          "vezes",
          "cometendo",
          "atos",
          "pela"
        ],
        "entities": [
          [
            "escolheu",
            "GPE"
          ],
          [
            "apenas",
            "GPE"
          ],
          [
            "simplesmente nasceu",
            "PERSON"
          ],
          [
            "nem cometeu \\n",
            "PERSON"
          ],
          [
            "mesmo de cometer",
            "ORG"
          ],
          [
            "mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 83.16639344262295,
        "semantic_density": 0,
        "word_count": 61,
        "unique_words": 52,
        "lexical_diversity": 0.8524590163934426
      },
      "preservation_score": 1.5810445081318458e-06
    },
    {
      "id": 1,
      "text": "Capítulo 6   \\nAqueles liderados com amor e ganância   \\nAqueles que seguem a herança do próprio sentimento ao \\nserem líderes fazem grande diferença social entre os liderados. \\nComo dito antes, aqueles líderes grandes se tornaram grandes \\natravés da confiança, logo, a forma de viver a própria vida é tão \\ngrandiosa q ue é vista de  uma forma a ser copiada ou imitada por \\naqueles que não conseguem enxergar que a sua forma de liderar \\nnão está atrelada à falta de competência, e sim ao dom de ser líder. \\nAqueles que chegam a uma liderança através de uma virtude não \\nconquista da por si próprio não tiveram uma vida miserável como \\nexemplo a ser seguida. Assim, esses humanos não são de \\nconfiança devido à falta de semelhança com o viver miserável.   \\n“Nosso caos vivido em cada território nos faz ter vários líderes \\ndiferentes próximos um do outro, ocasionando interesses de \\ndiferença  \\nextrema entre vizinhos.”   \\nEssa frase citada acima me faz pensar em vários \\nquestionamentos diferentes, em várias frentes de pensamentos e \\nisso ocorre devido às diferenças dos trajetos evolutivos,",
      "position": 22707,
      "chapter": 6,
      "page": 22,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.331638418079095,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 29.5,
        "avg_word_length": 4.994350282485875,
        "unique_word_ratio": 0.6836158192090396,
        "avg_paragraph_length": 177.0,
        "punctuation_density": 0.07344632768361582,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "aqueles",
          "líderes",
          "forma",
          "liderados",
          "próprio",
          "diferença",
          "entre",
          "como",
          "grandes",
          "através",
          "confiança",
          "viver",
          "vida",
          "falta",
          "miserável",
          "devido",
          "vários",
          "diferentes",
          "capítulo",
          "amor"
        ],
        "entities": [
          [
            "6",
            "CARDINAL"
          ],
          [
            "ganância   \\nAqueles",
            "PERSON"
          ],
          [
            "tão \\ngrandiosa",
            "ORG"
          ],
          [
            "vista de  uma forma",
            "ORG"
          ],
          [
            "falta de semelhança",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "ocasionando",
            "GPE"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 83.75169491525423,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 121,
        "lexical_diversity": 0.6836158192090396
      },
      "preservation_score": 1.0728516305180385e-05
    },
    {
      "id": 1,
      "text": "“involuídos” (algo que regressou o que  \\nevoluiu) e “desvoluídos” (algo que era para ter evoluído mais do \\nque evoluiu) que cada território teve que passar para conseguir \\nsobreviver melhor do que se vivia, transformando, assim, a \\nmiséria dos miseráveis em necessária  para o sistema de produção \\nmundial de um viver melhor e outros piores como necessários \\npara se ter desde comida, sexo, ódio, amor, felicidade, tristeza, \\nfamília, amigos e  tudo o que nos faz ser humanos.   \\nAssim, voltamos ao assunto das virtudes dos líderes, \\naquelas que foram conquistadas com sinceridade, amor, \\nfelicidade, compaixão, empatia e aquelas virtudes consideradas \\nhonestas e boas pela maioria dos miseráveis. Esse c ontexto será \\nde fácil liderança devido à facilidade dos liderados. Esses \\nliderados não são miseráveis, ao contrário, são gratos por serem \\nbem instruídos e reconhecem a dignidade de viver uma vida \\nmútua com um grande líder a ser seguido. Essa dinâmica inser e \\nesses sujeitos em uma única engrenagem e não em várias, pois na \\nvida sempre iniciamos algo em algum momento. Esse início tem \\numa direção a ser seguida de acordo com o trajeto que foi \\ndirecionado, logo, todo movimento de um líder tem que ser mútuo \\ncom tod os os liderados e, quando se tem um encaixe sentimental",
      "position": 23953,
      "chapter": 1,
      "page": 23,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.77463768115942,
      "complexity_metrics": {
        "word_count": 207,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.5,
        "avg_word_length": 5.082125603864735,
        "unique_word_ratio": 0.6618357487922706,
        "avg_paragraph_length": 207.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "algo",
          "miseráveis",
          "liderados",
          "evoluiu",
          "melhor",
          "assim",
          "viver",
          "amor",
          "felicidade",
          "virtudes",
          "aquelas",
          "esse",
          "esses",
          "vida",
          "líder",
          "involuídos",
          "regressou",
          "desvoluídos",
          "evoluído",
          "mais"
        ],
        "entities": [
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "para o",
            "PERSON"
          ],
          [
            "sistema de produção",
            "ORG"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Assim",
            "ORG"
          ],
          [
            "das",
            "ORG"
          ],
          [
            "dignidade",
            "CARDINAL"
          ],
          [
            "Essa",
            "PERSON"
          ]
        ],
        "readability_score": 81.22536231884058,
        "semantic_density": 0,
        "word_count": 207,
        "unique_words": 137,
        "lexical_diversity": 0.6618357487922706
      },
      "preservation_score": 2.6350741802197434e-05
    },
    {
      "id": 1,
      "text": "entre o movimentar -se de um líder com os liderados, todos os \\nmovimentos conspiram a favor do líder.   \\n“Já para  o líder que lidera pela ganância, usar palavras sem poder \\nmonetário é o suicídio das  \\npróprias palavras.”   \\nDaí resulta que todos os líderes que conquistaram a \\nliderança através da ganância fizeram isso através da confiança \\nmonetária, quando se tem confiança através do monetário ela se \\nperde quando há ausência do monetário.    \\nPorém, superar aqueles que invejam as suas condições de \\nlíder é necessário, os seus grandes feitos monetários serão \\naspectos de veneração por aqueles que tinham inveja da sua \\ncondição. Os mesmos humanos que tiveram a ganância como \\nimpulso foram dignos de serem admirados,  pois aquela mesma \\nsituação que poderia ter sido causa de inveja foi a causa que o fez \\nser poderoso, seguro, honrado e feliz, isso nos faz lembrar de \\ngrandes líderes miseráveis.  \\nEsses humanos são aqueles que, com o sentimento de caos \\nsemelhante, conquista ram os liderados, o mesmo caos que \\nassombrou a miséria também assombrou o bom líder ganancioso.",
      "position": 25352,
      "chapter": 1,
      "page": 24,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.03121387283237,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 28.833333333333332,
        "avg_word_length": 5.104046242774566,
        "unique_word_ratio": 0.6763005780346821,
        "avg_paragraph_length": 173.0,
        "punctuation_density": 0.10404624277456648,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "ganância",
          "monetário",
          "através",
          "aqueles",
          "liderados",
          "todos",
          "palavras",
          "líderes",
          "isso",
          "confiança",
          "quando",
          "grandes",
          "inveja",
          "humanos",
          "causa",
          "caos",
          "assombrou",
          "entre",
          "movimentar"
        ],
        "entities": [
          [
            "entre o movimentar -se",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Já",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "monetário ela",
            "PERSON"
          ],
          [
            "perde quando",
            "PERSON"
          ],
          [
            "ausência",
            "GPE"
          ],
          [
            "monetário",
            "GPE"
          ],
          [
            "Porém",
            "PERSON"
          ]
        ],
        "readability_score": 84.05211946050096,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 117,
        "lexical_diversity": 0.6763005780346821
      },
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "id": 1,
      "text": "“O nosso valor monetário não se compara ao de um líder que já \\nvem com o dom da liderança, porém um dom sem saber \\nadministrar os seus  \\nimpulsos é igual falar d e um sábio tolo...”",
      "position": 26555,
      "chapter": 1,
      "page": 25,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.433333333333334,
      "complexity_metrics": {
        "word_count": 36,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 18.0,
        "avg_word_length": 3.9444444444444446,
        "unique_word_ratio": 0.9166666666666666,
        "avg_paragraph_length": 36.0,
        "punctuation_density": 0.1111111111111111,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "valor",
          "monetário",
          "compara",
          "líder",
          "liderança",
          "porém",
          "saber",
          "administrar",
          "seus",
          "impulsos",
          "igual",
          "falar",
          "sábio",
          "tolo"
        ],
        "entities": [
          [
            "monetário não se compara ao de",
            "PERSON"
          ]
        ],
        "readability_score": 89.81666666666666,
        "semantic_density": 0,
        "word_count": 36,
        "unique_words": 33,
        "lexical_diversity": 0.9166666666666666
      },
      "preservation_score": 6.775905034850767e-07
    },
    {
      "id": 1,
      "text": "Capítulo 7   \\nComo evitar que a ganância se afortune de outras ganâncias \\nalheias    \\nAquele que se afortuna através do erro ganancioso de um \\nlíder se torna escravo da ambição, pois isso requer muito esforço \\nmental e corpóreo para manter em funcionamento diante de sua \\nambição. Ao inventar novas ideias com a finalidade de ganhar \\nmais fortuna , precisa -se de muito esforço de um miserável que \\nnão percebe seu erro para a ganância ruim.   \\nComo percebemos ao decorrer deste livro, estamos \\nvivendo tantos erros “pequenos” que, muitas vezes, não damos \\ntanta atenção, até porque estamos tão acostumados a viver em um \\nsistema que nos faz enxergar o que o próprio sistema direciona \\nque esquecemos das limitações criadas pela ganância de quem \\nprecisa de “mais ganância”. Isso gera um sistema cíclico de \\nlimitações criado pelo próprio sistema, devido ao próprio sistema \\nnão conseguir limitar o próprio sistema cíclico de adaptação do \\ninício de um movimento.",
      "position": 26938,
      "chapter": 7,
      "page": 26,
      "segment_type": "page",
      "themes": {},
      "difficulty": 47.781168831168834,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 38.5,
        "avg_word_length": 5.103896103896104,
        "unique_word_ratio": 0.6818181818181818,
        "avg_paragraph_length": 154.0,
        "punctuation_density": 0.07142857142857142,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sistema",
          "ganância",
          "próprio",
          "como",
          "erro",
          "ambição",
          "isso",
          "muito",
          "esforço",
          "mais",
          "precisa",
          "estamos",
          "limitações",
          "cíclico",
          "capítulo",
          "evitar",
          "afortune",
          "outras",
          "ganâncias",
          "alheias"
        ],
        "entities": [
          [
            "Aquele",
            "GPE"
          ],
          [
            "se afortuna",
            "PERSON"
          ],
          [
            "requer muito esforço",
            "PERSON"
          ],
          [
            "diante de sua \\nambição",
            "PERSON"
          ],
          [
            "mais fortuna",
            "PERSON"
          ],
          [
            "precisa -se de muito esforço de um miserável que",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "estamos \\nvivendo",
            "PERSON"
          ],
          [
            "não damos",
            "PERSON"
          ],
          [
            "tão",
            "ORG"
          ]
        ],
        "readability_score": 79.21883116883117,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 105,
        "lexical_diversity": 0.6818181818181818
      },
      "preservation_score": 1.0239145385996715e-05
    },
    {
      "id": 1,
      "text": "“Temos o líder miserável pela ganância gerada pelo excesso de \\ntrabalho que  o torna cego para uma evolução de liderar em  vez de \\ntrabalhar ...”   \\nQuando se conquista uma liderança pela miséria e na \\nmiséria se permanece, essa mesma miséria irá limitar a sua \\nliderança, pois essa mesma miséria que o fez grande é a mesma \\nmiséria que te torna um líder miserável. Logo, percebemos que \\nquando se torna um líder miserável no mesmo nicho social \\nmiserável, temos que negociar para manter uma liderança \\nmiserável. Conforme o nível de um líder miserável começa a ser \\nreconhecido como líder com líderes ele tem que se misturar, pois \\nindependente da ganância ser sentimental ou monetária, ambas \\ndemonstram tipos de ser um grande líder. Venho de um exemplo \\na ser seguido para aqueles  miseráveis que os querem seguir.   \\nA ganância alheia não veio de uma simples ganância, e \\nsim de uma ganância invejosa, que foi criada através de enxergar \\n“a grama do vizinho sempre é mais verde”. Assim como foi dito \\nantes, muitos enxergam a vida de outro como exemplo: qual seria \\nesse exemplo? Esse exemplo pode ser devido à inveja do \\nmiserável pelo líder ser pelo monetário ganancioso, assim como",
      "position": 28060,
      "chapter": 1,
      "page": 27,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.83712121212121,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 24.75,
        "avg_word_length": 4.873737373737374,
        "unique_word_ratio": 0.6161616161616161,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.10101010101010101,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "miserável",
          "ganância",
          "miséria",
          "como",
          "exemplo",
          "pelo",
          "torna",
          "liderança",
          "mesma",
          "temos",
          "pela",
          "quando",
          "essa",
          "pois",
          "grande",
          "assim",
          "esse",
          "gerada",
          "excesso"
        ],
        "entities": [
          [
            "pela ganância gerada pelo excesso de \\ntrabalho",
            "PERSON"
          ],
          [
            "vez de \\ntrabalhar",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "essa mesma",
            "ORG"
          ],
          [
            "miséria irá limitar",
            "PERSON"
          ],
          [
            "essa mesma miséria",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "negociar para manter",
            "PERSON"
          ],
          [
            "querem seguir",
            "PERSON"
          ]
        ],
        "readability_score": 86.16287878787878,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 122,
        "lexical_diversity": 0.6161616161616161
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "por sua casa, seu carro, seu dinheiro e tudo em nosso estilo \\nganancioso de viver a vida nos torna grandes. Isso, no entanto, \\ncausa a inveja de outros líderes gananciosos.   \\nNem toda liderança precisa ser grande, mas também não \\ndeve ser tão pequena de modo a não chegar a ser liderança, assim \\ncomo a simplicidade de um grande líder o torna grande, ela \\ntambém limita. Log o, enxergamos que a decadência de um líder \\né ficar estável na própria liderança, assim como os miseráveis \\nevoluem para ser liderados, os liderados evoluem para serem \\nlíderes. Assim, ocorre a necessidade de quem é líder evoluir em \\nser líder, não saber lidar  com a evolução o faz criar regras por não \\nsaber liderar, gerando mais caos devido a um viver infeliz.     \\nDesse modo, isso nos faz perceber que viver feliz na \\nmiséria é a maior motivação que pode se ter em um viver sendo \\num bom miserável. Logo, enxergamos  que na miséria não se pode \\nter muitas regras, pois o excesso delas o faz desistir da própria \\nmiséria, assim como o líder quer viver com liberdade, o miserável \\ntambém quer. Porém, temos uma questão: o miserável não pode \\nser livre. O excesso de liberdade pa ra um miserável é a falta de",
      "position": 29364,
      "chapter": 1,
      "page": 28,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.931206804891016,
      "complexity_metrics": {
        "word_count": 209,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.22222222222222,
        "avg_word_length": 4.559808612440191,
        "unique_word_ratio": 0.5980861244019139,
        "avg_paragraph_length": 209.0,
        "punctuation_density": 0.1339712918660287,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "líder",
          "assim",
          "miserável",
          "liderança",
          "grande",
          "também",
          "como",
          "miséria",
          "pode",
          "torna",
          "isso",
          "líderes",
          "modo",
          "enxergamos",
          "própria",
          "evoluem",
          "liderados",
          "saber",
          "regras"
        ],
        "entities": [
          [
            "por sua casa",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "mas também",
            "PERSON"
          ],
          [
            "ela \\ntambém limita",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "para serem",
            "PERSON"
          ],
          [
            "evoluir",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "criar",
            "PRODUCT"
          ]
        ],
        "readability_score": 87.02094630515683,
        "semantic_density": 0,
        "word_count": 209,
        "unique_words": 125,
        "lexical_diversity": 0.5980861244019139
      },
      "preservation_score": 1.897253409758215e-05
    },
    {
      "id": 1,
      "text": "evolução. Desse modo, ele não consegue fazer o trabalho \\ncorretamente, pois não é instruído por um líder para ser melhor.  \\nSendo assim, outra questão surge: o que fazer com o miserável \\nque é confortável com a miséria?   \\n“Nenhum humano, por mais miserável que ele seja, não tem algo \\nque queira melhorar na  \\nmediocridade da miséria.”   \\nTodos nós queremos chegar a uma estabilidade na vida, e \\nessa ganância pela estabilidade nos deixa instáveis pela \\nmediocridade na ganância humana em se r feliz. Essa busca pela \\nfelicidade humana nos impulsiona a conquistar uma grande \\nliderança, que é impulsionada pelos instintos primitivos do \\npróprio humano. Os mesmos humanos miseráveis sem controle \\nda sua própria histeria primitiva, devido à falta de con trole do seu \\npróprio corpo em querer sexo e comida melhores. Assim, se \\ntransformam em gananciosos por uma aparência de ter as pessoas \\nmais bonitas a sua volta, as casas mais bonitas, carros mais \\nbonitos, comer nos melhores restaurantes, melhores artes e tu do \\naquilo exclusivo de melhor que possam ter.",
      "position": 30667,
      "chapter": 1,
      "page": 29,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 27.16760355029586,
      "complexity_metrics": {
        "word_count": 169,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 21.125,
        "avg_word_length": 5.1420118343195265,
        "unique_word_ratio": 0.7100591715976331,
        "avg_paragraph_length": 169.0,
        "punctuation_density": 0.1301775147928994,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "pela",
          "melhores",
          "fazer",
          "melhor",
          "assim",
          "miserável",
          "miséria",
          "humano",
          "mediocridade",
          "estabilidade",
          "essa",
          "ganância",
          "humana",
          "próprio",
          "bonitas",
          "evolução",
          "desse",
          "modo",
          "consegue"
        ],
        "entities": [
          [
            "para ser melhor",
            "PERSON"
          ],
          [
            "Sendo",
            "PERSON"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "Nenhum",
            "ORG"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "nós queremos chegar",
            "ORG"
          ],
          [
            "essa ganância pela estabilidade",
            "PERSON"
          ],
          [
            "instáveis pela",
            "PERSON"
          ],
          [
            "ganância humana",
            "PERSON"
          ],
          [
            "humana",
            "ORG"
          ]
        ],
        "readability_score": 87.89489644970413,
        "semantic_density": 0,
        "word_count": 169,
        "unique_words": 120,
        "lexical_diversity": 0.7100591715976331
      },
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "id": 1,
      "text": "“O filho que é criado por um líder ganancioso exemplar vai querer \\nter uma maior ganância de  \\nliderança que a mãe.”   \\nO filho de um líder, quando criado através de um pai que \\né exemplo, esse mesmo exemplo gera  competição. O filho que se \\nengrandeceu através do caos de tabela devido à vida de um pai \\npode se tornar maior que a própria mãe. Para fazer isso, é \\nnecessário tampar os erros do próprio pai, pois o mesmo pai que \\no criou, ensinou a exercer a profissão a qu al ele levou uma vida \\npara aprender, o mesmo filho cresceu aprendendo sem esforço. \\nLogo, percebemos que a necessidade de aprendizado daquele que \\nestá aprendendo naturalmente leva a preencher os erros deixados \\nno trajeto do líder o qual está seguindo, assim  o tornando um líder \\nmais completo que o próprio pai. Não irei falar daquele que não \\ntem aptidão de ser um líder no direcionamento da mãe, até porque \\ntalvez ele seja um líder melhor em outro direcionamento em \\ncomparação ao pai.   \\nMas, lembre -se, uma mãe qu e é grande como líder, como \\nna maioria das vezes, não consegue ser um bom pai, pois pensa \\nem um viver “melhor para a família”, dando importância mais",
      "position": 31846,
      "chapter": 1,
      "page": 30,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.059163763066202,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.285714285714285,
        "avg_word_length": 4.482926829268293,
        "unique_word_ratio": 0.6097560975609756,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.1024390243902439,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "filho",
          "mesmo",
          "criado",
          "maior",
          "através",
          "exemplo",
          "vida",
          "erros",
          "próprio",
          "pois",
          "aprendendo",
          "daquele",
          "está",
          "mais",
          "direcionamento",
          "melhor",
          "como",
          "ganancioso",
          "exemplar"
        ],
        "entities": [
          [
            "ganância de  \\n",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "al ele levou",
            "PERSON"
          ],
          [
            "para aprender",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "naturalmente leva",
            "PERSON"
          ],
          [
            "Mas",
            "PERSON"
          ]
        ],
        "readability_score": 84.01226480836237,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 125,
        "lexical_diversity": 0.6097560975609756
      },
      "preservation_score": 1.8596094928979333e-05
    },
    {
      "id": 1,
      "text": "para o lado ganancioso devido ao medo da miséria. Assim como \\na sua liderança é digna, a família tem que es tar na mesma altura \\nde importância. Nós sentimos necessidade de criar os filhos, e \\nnossos filhos também têm a necessidade de cuidar de nós com \\namor, carinho, atenção, brincadeiras e tudo aquilo que só uma \\nmãe pode dar. Logo, vejo que a decadência de um líd er é a \\nausência de importância vinda daqueles que ele ama .   \\nA falta de um bom líder deixa os miseráveis sem direção \\ncoletiva, então de nada adianta uma liderança sem o trajeto da \\nconquista, pois esse trajeto cria alicerces necessários para ter \\njunto àqueles  liderados que os seguem, pois,  aqueles liderados \\nque ajudaram a conquistar a liderança através das dificuldades são \\nos que irão seguir na felicidade. Os mesmos que dão a vida por \\nvocê através da ganância, pela mesma ganância alcançaram a \\nliderança junto s ao líder e essa mesma liderança é julgada pelos \\nliderados. Logo, quanto mais o líder adquirir uma maior \\nliderança, maior haverá a necessidade de se trabalhar com   \\n“inimigos”, pois ao adquirir novas lideranças, maior será o \\nterritório a liderar, assim mo strando a necessidade de não chegar \\nà liderança através da ganância ou confiança, e sim com ambas \\nem equilíbrio constante, pois a dor de um é a dor do outro. Assim,",
      "position": 33111,
      "chapter": 1,
      "page": 31,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.482853982300885,
      "complexity_metrics": {
        "word_count": 226,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.25,
        "avg_word_length": 4.734513274336283,
        "unique_word_ratio": 0.6415929203539823,
        "avg_paragraph_length": 226.0,
        "punctuation_density": 0.11504424778761062,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liderança",
          "necessidade",
          "pois",
          "assim",
          "mesma",
          "líder",
          "liderados",
          "através",
          "ganância",
          "maior",
          "importância",
          "filhos",
          "logo",
          "trajeto",
          "junto",
          "adquirir",
          "lado",
          "ganancioso",
          "devido",
          "medo"
        ],
        "entities": [
          [
            "para o",
            "PERSON"
          ],
          [
            "lado ganancioso devido",
            "PERSON"
          ],
          [
            "medo da miséria",
            "PERSON"
          ],
          [
            "digna",
            "PERSON"
          ],
          [
            "altura \\nde importância",
            "PERSON"
          ],
          [
            "também têm",
            "ORG"
          ],
          [
            "necessidade de cuidar de nós",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "vejo que",
            "GPE"
          ],
          [
            "ausência de",
            "PERSON"
          ]
        ],
        "readability_score": 84.45464601769912,
        "semantic_density": 0,
        "word_count": 226,
        "unique_words": 145,
        "lexical_diversity": 0.6415929203539823
      },
      "preservation_score": 2.108059344175795e-05
    },
    {
      "id": 1,
      "text": "entendemos que a dor de cada miserável tem que ser equilibrada \\nentre a ganância e a confian ça, os miseráveis que eram \\n“inimigos”, após serem tratados como semelhantes dos liderados \\nmais antigos, sentem -se tão amados quanto os outros miseráveis \\nsão amados, o líder que consegue reconhecer essa forma de \\nliderar é o líder mais próximo de viver semel hante entre todos \\naqueles liderados.    \\nNós, humanos, somos movidos pelos desejos primitivos \\ncorpóreos, são eles que nos dizem quando queremos comer, \\ndormir e fazer sexo. Nossos desejos primitivos não nos deixam \\ncompreender quais são os benefícios e os mal efícios de uma \\nliderança, devido a não entendermos e compreendermos o valor \\ndos nossos pensamentos afetivos. Se conseguíssemos olhar e \\nenxergar esses valores não deixaríamos a ganância alheia destruir \\nnossa ganância, pois nossa ganância sendo satisfatória em um \\nviver de acordo com o próprio viver não tem como haver o lado \\nruim, e sim um equilíbrio da ganância.",
      "position": 34548,
      "chapter": 1,
      "page": 32,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.059615384615384,
      "complexity_metrics": {
        "word_count": 156,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 39.0,
        "avg_word_length": 5.198717948717949,
        "unique_word_ratio": 0.7115384615384616,
        "avg_paragraph_length": 156.0,
        "punctuation_density": 0.09615384615384616,
        "line_break_count": 16,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ganância",
          "viver",
          "entre",
          "miseráveis",
          "como",
          "liderados",
          "mais",
          "amados",
          "líder",
          "desejos",
          "primitivos",
          "nossos",
          "nossa",
          "entendemos",
          "cada",
          "miserável",
          "equilibrada",
          "confian",
          "eram",
          "inimigos"
        ],
        "entities": [
          [
            "após serem",
            "PERSON"
          ],
          [
            "tão",
            "PRODUCT"
          ],
          [
            "quanto os outros miseráveis",
            "PERSON"
          ],
          [
            "essa forma de \\nliderar",
            "PERSON"
          ],
          [
            "mais próximo de viver semel hante",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Nós",
            "ORG"
          ],
          [
            "quando queremos",
            "PERSON"
          ],
          [
            "mal",
            "ORG"
          ],
          [
            "Se conseguíssemos",
            "PERSON"
          ]
        ],
        "readability_score": 78.94038461538462,
        "semantic_density": 0,
        "word_count": 156,
        "unique_words": 111,
        "lexical_diversity": 0.7115384615384616
      },
      "preservation_score": 1.084144805576123e-05
    },
    {
      "id": 1,
      "text": "Capítulo 8    \\nAqueles que chegaram perto através da ganância ruim   \\n“Quando um líder chega à liderança por um meio criminoso pensa \\nque qualquer problema será resolvido através daquele erro \\ncriminoso, mas não sabe que será a causa de um crime  \\nmaior...”   \\nOs miseráveis que conseguiram uma liderança através de \\num dom, e não  pela compaixão de seus seguidores são os que \\ndeixam um rastro de atos de grandes extravagâncias, luxúrias, \\nostentação, egocentrismo e todos os sentimentos que nos trazem \\nmais bens materiais do que sentimentais.   \\n“O trajeto de um líder que conquistou sua liderança \\natravés de extravagâncias, as mesmas extravagâncias são \\ncriminalizadas pelos miseráveis que o admiram  por esse   estilo  \\nde  vida  extravagante.”   \\nA luxúria vivida por esse líder é julgada por liderados \\nreligiosos e conservadores e, até mesmo , pelos religiosos e \\nconservadores que têm uma liderança obrigatória e um estilo de \\nvida cheio de erros, desgraças, preconceitos, julgamentos e",
      "position": 35855,
      "chapter": 8,
      "page": 34,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.73228476821192,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 37.75,
        "avg_word_length": 5.357615894039735,
        "unique_word_ratio": 0.6490066225165563,
        "avg_paragraph_length": 151.0,
        "punctuation_density": 0.10596026490066225,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "através",
          "liderança",
          "líder",
          "extravagâncias",
          "criminoso",
          "será",
          "miseráveis",
          "pelos",
          "esse",
          "estilo",
          "vida",
          "religiosos",
          "conservadores",
          "capítulo",
          "aqueles",
          "chegaram",
          "perto",
          "ganância",
          "ruim",
          "quando"
        ],
        "entities": [
          [
            "8    \\nAqueles",
            "PERCENT"
          ],
          [
            "da ganância",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "mas não",
            "PERSON"
          ],
          [
            "compaixão de seus",
            "ORG"
          ],
          [
            "rastro de atos de",
            "ORG"
          ],
          [
            "mesmas",
            "PERSON"
          ],
          [
            "pelos miseráveis",
            "PERSON"
          ],
          [
            "julgada",
            "PERSON"
          ],
          [
            "até mesmo",
            "PERSON"
          ]
        ],
        "readability_score": 79.51771523178809,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 98,
        "lexical_diversity": 0.6490066225165563
      },
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "id": 1,
      "text": "muitos outros incômodos derivados do próprio estilo de vida de \\ntanta certeza.   \\nO que seria um líder vencedor?   \\nDe nada adianta vencer uma liderança através da ganância \\nsem ter o sentimento por aqueles que estão perto, pois as ações e \\na vida desse líder não encontrarão sentido ou acharão muito pouco \\nque possa contribuir para a liderança. A mesma liderança que com \\npouco esforço se conquistou é também aquela que com \\nfacilidades foi conquistada, não facilidade no sentido de ser fácil, \\ne sim de querer se dar bem diante das situações as quais vê \\nfacilidades em ser beneficiado. Esse benefício não está atrelado a \\num contex to, e sim para si mesmo, pois ao conquistar uma \\nliderança sem esforço, não se estabelece semelhança com o \\nmiserável que te protege, não por poder, mas sim por quantidade \\nde miseráveis liderados.    \\nLogo, os miseráveis não simpatizando com o líder \\nconquista  a liderança pela ostentação de um viver a vida e chega \\nà liderança por meio daqueles que têm uma fortuna maior que os \\nmiseráveis. Esses sujeitos são chamados de classe média alta ou \\nbaixa e, por muitas vezes, também são chamados de pobres, mas",
      "position": 37007,
      "chapter": 1,
      "page": 35,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.162723214285712,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.428571428571427,
        "avg_word_length": 4.828125,
        "unique_word_ratio": 0.65625,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.09375,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liderança",
          "vida",
          "líder",
          "miseráveis",
          "pois",
          "sentido",
          "pouco",
          "esforço",
          "também",
          "facilidades",
          "chamados",
          "muitos",
          "outros",
          "incômodos",
          "derivados",
          "próprio",
          "estilo",
          "tanta",
          "certeza",
          "seria"
        ],
        "entities": [
          [
            "muitos outros incômodos",
            "ORG"
          ],
          [
            "acharão muito pouco \\nque",
            "PERSON"
          ],
          [
            "também aquela",
            "PERSON"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "sentido de ser",
            "PERSON"
          ],
          [
            "diante das situações",
            "PERSON"
          ],
          [
            "não se estabelece semelhança",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "têm uma fortuna maior",
            "ORG"
          ]
        ],
        "readability_score": 84.83727678571428,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 126,
        "lexical_diversity": 0.65625
      },
      "preservation_score": 1.2874219566216461e-05
    },
    {
      "id": 1,
      "text": "não consegu em enxergar a ostentação diante da própria vida \\nmiserável em que vivem por não saber controlar o desejo de ser \\nmelhor do que aquele que precisa evoluir junto. Assim, perdem -\\nse em uma vida egocêntrica com seguidores egocêntricos, ambos \\nos lados entram em um a competição de um viver melhor e, em \\ndiversos casos, nem sabem mais o que é melhor, já que buscam \\nsempre mais de tanto ter mais, sobre ser mais daquilo a qual não \\nvão contribuir em nada no seu viver, só interferindo em qualquer \\ncoisa a mais que aquele ego centrismo possa ser ou ter, maior que \\no outro egocêntrico.   \\nTodas essas características citadas acima estão associadas \\nao caráter que deixa um legado e, ao mesmo tempo, deixa um \\nrastro de caos. Isso ocorre, pois ele tem excessos de problemas e \\né admirado por outros líderes que têm o mesmo amor pelas coisas \\nque aquele líder exemplar tem em relação às extravagâncias do \\negocentrismo.   \\nQuando  um  líder  se  perde  nas \\nextravagâncias da liderança não perde só bens materiais, mas \\ntambém sentimentais, pois essa  liderança conquistada com \\n“facilidade” é a mesma que causa desconforto para aqueles que",
      "position": 38268,
      "chapter": 1,
      "page": 36,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.740932642487046,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 38.6,
        "avg_word_length": 4.803108808290156,
        "unique_word_ratio": 0.6735751295336787,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.08808290155440414,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "melhor",
          "aquele",
          "vida",
          "viver",
          "deixa",
          "mesmo",
          "pois",
          "líder",
          "extravagâncias",
          "perde",
          "liderança",
          "consegu",
          "enxergar",
          "ostentação",
          "diante",
          "própria",
          "miserável",
          "vivem",
          "saber"
        ],
        "entities": [
          [
            "desejo de ser \\nmelhor",
            "ORG"
          ],
          [
            "diversos casos",
            "PERSON"
          ],
          [
            "nem sabem mais",
            "PERSON"
          ],
          [
            "sempre mais de tanto",
            "PERSON"
          ],
          [
            "nada no",
            "ORG"
          ],
          [
            "qualquer \\ncoisa",
            "PERSON"
          ],
          [
            "outro egocêntrico",
            "PERSON"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "características",
            "GPE"
          ],
          [
            "acima estão associadas",
            "PERSON"
          ]
        ],
        "readability_score": 79.25906735751295,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 130,
        "lexical_diversity": 0.6735751295336787
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "o fazem feliz, perdendo -se, assim, na tristeza de um estilo de \\nvida que enxerga a felicidade dentro da tristeza, tornando -se \\nextravagante devido ao caos vivido para se  ter aquele momento \\nde felicidade.   \\nQuando um grande líder miserável não sabe diferenciar os \\nseus acertos e as suas falhas, logo a falta de avaliação de certo ou \\nerrado o limita em viver melhor, pois a falta de acerto com \\npessoas próximas significa não re conhecer o que pode ser \\nprejudicial.  Por não saber limitar questões que podem ocasionar \\nerros e ofensas que se tornaram necessárias durante o trajeto. São \\nessas questões que fazem diversos líderes temerem o próprio \\nviver, uma vez que estão diante de vário s problemas que levam a \\num ciclo infinito de desconfiança, tornando -se uma pessoa \\nsolitária não pelas extravagâncias, e sim por não ter confiança em \\nser feliz.",
      "position": 39531,
      "chapter": 1,
      "page": 37,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.339335664335664,
      "complexity_metrics": {
        "word_count": 143,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 35.75,
        "avg_word_length": 4.881118881118881,
        "unique_word_ratio": 0.7342657342657343,
        "avg_paragraph_length": 143.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 14,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazem",
          "feliz",
          "tristeza",
          "felicidade",
          "tornando",
          "falta",
          "viver",
          "questões",
          "perdendo",
          "assim",
          "estilo",
          "vida",
          "enxerga",
          "dentro",
          "extravagante",
          "devido",
          "caos",
          "vivido",
          "aquele",
          "momento"
        ],
        "entities": [
          [
            "para se  ",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "de avaliação de certo",
            "ORG"
          ],
          [
            "limitar",
            "ORG"
          ],
          [
            "fazem diversos",
            "ORG"
          ],
          [
            "diante de vário s problemas",
            "PERSON"
          ],
          [
            "infinito de desconfiança",
            "ORG"
          ]
        ],
        "readability_score": 80.66066433566434,
        "semantic_density": 0,
        "word_count": 143,
        "unique_words": 105,
        "lexical_diversity": 0.7342657342657343
      },
      "preservation_score": 8.432237376703178e-06
    },
    {
      "id": 1,
      "text": "Capítulo 9    \\nOs miseráveis   \\n“Todos aqueles miseráveis que se transformam em fãs de uma \\nliderança são aqueles que  \\nnasceram para ser miseráveis.”   \\n  Qualquer ordem padrão de um direcionamento territorial \\nfoi ocasionada devido a uma maior massa pensar semelhante ao \\nconflito gerado pe lo líder, já que ele quer viver uma ganância \\nconfortável. O mesmo conforto que nos faz mal é o mesmo que \\nnos transforma em miseráveis afortunados, pois os miseráveis na \\nmiséria não veem evolução na miséria em que vivem.   \\nQuando se é miserável, não há opçã o, e sim a necessidade \\nde viver.  Quando se tem a necessidade de viver com o que já se \\ntem, há a necessidade de aceitar as tendências adversas da vida e \\nisso resulta em um cenário em que os miseráveis não querem ser \\nreprimidos, mas viver o melhor dentro da  miséria a qual se \\nencontram. Desse modo, isso nos faz enxergar a necessidade de \\naceitar a opressão gerada por um líder. O líder, quando é bom, \\nsabe direcionar os problemas e outros líderes, quando não sabe \\ndirecionar a miséria é atingido, uma vez que a mi séria não o",
      "position": 40523,
      "chapter": 9,
      "page": 38,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.39327731092437,
      "complexity_metrics": {
        "word_count": 187,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 26.714285714285715,
        "avg_word_length": 4.641711229946524,
        "unique_word_ratio": 0.5828877005347594,
        "avg_paragraph_length": 187.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "viver",
          "miséria",
          "quando",
          "necessidade",
          "líder",
          "aqueles",
          "mesmo",
          "aceitar",
          "isso",
          "sabe",
          "direcionar",
          "capítulo",
          "todos",
          "transformam",
          "liderança",
          "nasceram",
          "qualquer",
          "ordem",
          "padrão"
        ],
        "entities": [
          [
            "9    \\n",
            "DATE"
          ],
          [
            "para ser miseráveis",
            "PRODUCT"
          ],
          [
            "Qualquer",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "não querem",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "problemas e outros líderes",
            "ORG"
          ]
        ],
        "readability_score": 85.25034377387318,
        "semantic_density": 0,
        "word_count": 187,
        "unique_words": 109,
        "lexical_diversity": 0.5828877005347594
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "deixará evoluir para ser um líder melhor. Além de serem \\nliderados, os miseráveis não querem ser oprimidos pelos líderes, \\nmas sim compreendidos por eles. Devido a essa necessidade de \\nserem liderados e compreendidos, ocorrem três efeitos adversos : \\nmiséria, liberdade ou desordem.    \\nUm líder não é só uma direção a ser seguida, e sim uma \\nexpansão do seu próprio caráter. Logo, entendemos que a \\nexpansão do apetite por uma liderança significa a evolução dos \\nmiseráveis. Eles sobrevivem apenas através de  um líder, não \\nconseguem se defender, mas enxergam o líder como a maior \\ndivindade  \\n(efeito fã, ficam cegos diante da própria vida).   \\nUm miserável se torna mais miserável quando não \\npercebe que a sua posição social está associada ao fato de não \\nenxergar qu e viver melhor na miséria é viver melhor com todos \\nos miseráveis sábios e inteligentes, não deixando de lembrar que \\no sábio é necessário para um grupo de miseráveis e o miserável \\ninteligente para outro grupo de miseráveis. Ambos os miseráveis \\nsão important es para a evolução territorial, nunca deixando de \\nlembrar que são muitos os miseráveis inteligentes que são",
      "position": 41766,
      "chapter": 1,
      "page": 39,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.021195652173915,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.0,
        "avg_word_length": 5.070652173913044,
        "unique_word_ratio": 0.6358695652173914,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.10326086956521739,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "líder",
          "melhor",
          "miserável",
          "serem",
          "liderados",
          "compreendidos",
          "eles",
          "miséria",
          "expansão",
          "evolução",
          "viver",
          "inteligentes",
          "deixando",
          "lembrar",
          "grupo",
          "deixará",
          "evoluir",
          "além",
          "querem"
        ],
        "entities": [
          [
            "deixará",
            "GPE"
          ],
          [
            "evoluir para",
            "PERSON"
          ],
          [
            "Além de serem",
            "PERSON"
          ],
          [
            "não querem ser oprimidos pelos líderes",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "desordem",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "Eles",
            "PERSON"
          ],
          [
            "da própria",
            "PERSON"
          ]
        ],
        "readability_score": 86.97880434782608,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 117,
        "lexical_diversity": 0.6358695652173914
      },
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "id": 1,
      "text": "enganosos devido a sua inteligência ser de serventia para si \\nmesmos. Assim, nos fazem viver em constante conflitos de \\ninteresses, por meio da ideia da existência de uma inteligência \\nmelhor que a nossa ou mais evoluída que a nossa, assim julgando \\na miséria alheia como uma melhor miséria em um sobreviver \\nmelhor.   \\nQuando os miseráveis, ardilosamente, não se obrigam por \\nambição é sinal de que pensam mais  em viver melhor com os \\nhumanos do que aqueles miseráveis inteligentes, pois eles não \\nenxergam aqueles liderados necessários, já que eles não têm \\nvalores monetários semelhantes. Esses liderados são os mesmos \\nque catam o nosso lixo, arrumam nossas casas, co letam um lixo \\nque ninguém quer coletar, limpam a fossa que os miseráveis \\njogam os seus excessos e tudo isso devido à perda de ver o nosso \\npróprio viver, o mesmo viver que faz esquecer os liderados e que \\nnos faz ter uma melhor vida miserável.   \\nAqueles lide rados semelhantes a um cavalo de corrida são \\nos melhores miseráveis que podemos ter ao nosso lado. Eles \\nfazem o trabalho dignamente, não precisam fazer muitas tarefas, \\npois não conseguem fazer muitas atividades ao mesmo tempo.",
      "position": 43024,
      "chapter": 2,
      "page": 40,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 32.4088132635253,
      "complexity_metrics": {
        "word_count": 191,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 31.833333333333332,
        "avg_word_length": 4.973821989528796,
        "unique_word_ratio": 0.6387434554973822,
        "avg_paragraph_length": 191.0,
        "punctuation_density": 0.09947643979057591,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "viver",
          "miseráveis",
          "aqueles",
          "eles",
          "liderados",
          "nosso",
          "devido",
          "inteligência",
          "mesmos",
          "assim",
          "fazem",
          "nossa",
          "mais",
          "miséria",
          "pois",
          "semelhantes",
          "lixo",
          "mesmo",
          "fazer"
        ],
        "entities": [
          [
            "enganosos devido",
            "PERSON"
          ],
          [
            "ser de serventia",
            "ORG"
          ],
          [
            "para si \\nmesmos",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "mesmos \\nque",
            "PERSON"
          ],
          [
            "lixo",
            "ORG"
          ],
          [
            "lixo",
            "ORG"
          ],
          [
            "perda de ver",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 82.5911867364747,
        "semantic_density": 0,
        "word_count": 191,
        "unique_words": 122,
        "lexical_diversity": 0.6387434554973822
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "Assim, o pouco que fazem é o suficiente para não se ter erros \\ndiante do trabalho que está sendo executado. Logo, percebemos \\nque o miserável que faz muitas tarefas, muitas tarefas serão mal \\nexecutadas, até porque são os líderes que realizam bem muitas \\nações.   \\nA falta de conhecimento s obre nós mesmos nos \\ntransforma em pessoas cheias de erros, os mesmos erros que nos \\nmoldam, que nos trazem os medos, traumas, depressão, \\nansiedade, cobrança ruim, caráter ruim e todas as nossas certezas \\nque nos tornam pessoas cegas diante da própria certeza , a mesma \\ncerteza falha que, quando a enxergamos como errada, não \\nconseguimos aceitar, não por interesse, e sim pela dor que nos \\ncausa entender aquele erro. Consequentemente, os mesmos erros \\nnão vistos e não querendo ser vistos transformam -nos em \\nmiserávei s solitários pela quantidade de erros não vistos por viver \\ncom outros miseráveis. Logo, o miserável solitário nem sempre é \\nsolitário pelos erros, e sim por sempre estar certo diante de outros \\nmiseráveis. Esse mesmo miserável solitário geralmente é o mais \\ninteligente, não pela quantidade de tarefas que faz, e sim por não \\nter paciência com outros miseráveis com os quais precisa viver.",
      "position": 44304,
      "chapter": 2,
      "page": 41,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 32.84710884353741,
      "complexity_metrics": {
        "word_count": 196,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.666666666666664,
        "avg_word_length": 5.045918367346939,
        "unique_word_ratio": 0.6122448979591837,
        "avg_paragraph_length": 196.0,
        "punctuation_density": 0.1377551020408163,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "erros",
          "diante",
          "miserável",
          "muitas",
          "tarefas",
          "mesmos",
          "pela",
          "vistos",
          "outros",
          "miseráveis",
          "solitário",
          "logo",
          "pessoas",
          "ruim",
          "certeza",
          "quantidade",
          "viver",
          "sempre",
          "assim",
          "pouco"
        ],
        "entities": [
          [
            "Logo",
            "PERSON"
          ],
          [
            "percebemos \\nque",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "executadas",
            "PRODUCT"
          ],
          [
            "mesmos erros",
            "GPE"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "cobrança ruim",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "Consequentemente",
            "PERSON"
          ],
          [
            "mesmos erros",
            "PERSON"
          ]
        ],
        "readability_score": 82.15289115646259,
        "semantic_density": 0,
        "word_count": 196,
        "unique_words": 120,
        "lexical_diversity": 0.6122448979591837
      },
      "preservation_score": 2.002656376967005e-05
    },
    {
      "id": 1,
      "text": "Os miseráveis sábios que administram uma família com \\nexcesso de dinheiro precisam controlar a sua própria ganância, \\npois aqu ela ganância necessária para a sua evolução em um viver \\nmelhor através da sabedoria passa ganância para aqueles de sua \\nfamília, já que o próprio sábio miserável não teve sabedoria para \\nensinar aqueles que precisavam ser ensinados a viver com o \\nexcesso. Log o, aqueles que são próximos tornam -se miseráveis \\ngananciosos sem sabedoria. O miserável sábio não pode se basear \\nsempre na “sabedoria”, pois essa mesma sabedoria que o fez ter a \\nfelicidade monetária é a própria enganação do sofrimento, já que \\no sábio miser ável não enxerga a dificuldade de manter aqueles \\nmiseráveis de sua família através do monetário. Assim, não \\npercebe que o mesmo monetário que o fez ser próximo daqueles \\nque ama, também o faz se afastar daqueles que um dia amou. \\nLogo, o nível de miserável s ábio que ele conquistou transforma \\nse em um miserável na miséria, não por causa do dinheiro, e sim \\npor perder aqueles que o transformaram em sábio.   \\nAssim, chegamos a um pensamento que um líder hábil \\ndeve equilibrar -se de uma maneira pela qual possa fazer  com \\nque os seus liderados sempre e em qualquer circunstância",
      "position": 45627,
      "chapter": 2,
      "page": 42,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.440453074433655,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.333333333333336,
        "avg_word_length": 4.893203883495145,
        "unique_word_ratio": 0.5922330097087378,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.07766990291262135,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sabedoria",
          "aqueles",
          "sábio",
          "miserável",
          "miseráveis",
          "família",
          "ganância",
          "excesso",
          "dinheiro",
          "própria",
          "pois",
          "viver",
          "através",
          "sempre",
          "monetário",
          "assim",
          "daqueles",
          "sábios",
          "administram",
          "precisam"
        ],
        "entities": [
          [
            "ela ganância necessária",
            "PERSON"
          ],
          [
            "passa ganância para aqueles de sua",
            "PERSON"
          ],
          [
            "ensinar aqueles",
            "PERSON"
          ],
          [
            "essa mesma sabedoria",
            "ORG"
          ],
          [
            "sábio miser",
            "PERSON"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "mesmo monetário que o fez",
            "PERSON"
          ],
          [
            "próximo daqueles \\n",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 81.3653721682848,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 122,
        "lexical_diversity": 0.5922330097087378
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "tenham necessidade de ser liderados e direcionados e, assim, \\neles sempre serão fiéis.",
      "position": 46978,
      "chapter": 2,
      "page": 43,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.184615384615384,
      "complexity_metrics": {
        "word_count": 13,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 13.0,
        "avg_word_length": 5.615384615384615,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.23076923076923078,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tenham",
          "necessidade",
          "liderados",
          "direcionados",
          "assim",
          "eles",
          "sempre",
          "serão",
          "fiéis"
        ],
        "entities": [
          [
            "tenham necessidade de ser",
            "PERSON"
          ]
        ],
        "readability_score": 91.81538461538462,
        "semantic_density": 0,
        "word_count": 13,
        "unique_words": 13,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.1293175058084612e-07
    },
    {
      "id": 1,
      "text": "Capítulo 10   \\nComo saber o tamanho da liderança   \\nComo já foi dito antes, para examinar o tamanho da \\nliderança, convém fazer uma outra consideração, isto é, se um \\nlíder tem uma liderança territorial grande para manter -se seguro \\njuntamente com outros líderes secundários,  lembrando que \\naqueles líderes secundários em volta de um maior líder são \\naqueles que se transformam em escudos humanos contra os \\nmalefícios que acompanham o trajeto de uma grande liderança. \\nSe organizar para ser um grande líder exige ter líderes secundári os \\nà altura da liderança exercida, a liderança que cobra muito tempo \\ndo líder é aquela que requer tempo para se pensar melhor. Logo, \\na mesma cobrança não permite ter conforto para pensar em \\nsoluções  para uma vivência melhor  daqueles liderados e \\nmiserávei s.   \\nAssim, aqueles miseráveis de diferentes classes sociais \\nsão o alimento da própria ganância, pois são muitos e, assim, \\ncontrolar a diferença social na miséria torna -se uma histeria \\nprimitiva coletiva dentro de uma miséria gananciosa por falta do \\nprópri o controle básico de ter sexo e comida.  Essa mesma histeria",
      "position": 47242,
      "chapter": 10,
      "page": 44,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.34550561797753,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 35.6,
        "avg_word_length": 5.151685393258427,
        "unique_word_ratio": 0.6629213483146067,
        "avg_paragraph_length": 178.0,
        "punctuation_density": 0.08426966292134831,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liderança",
          "líder",
          "grande",
          "líderes",
          "aqueles",
          "como",
          "tamanho",
          "secundários",
          "tempo",
          "pensar",
          "melhor",
          "mesma",
          "assim",
          "miséria",
          "histeria",
          "capítulo",
          "saber",
          "dito",
          "antes",
          "examinar"
        ],
        "entities": [
          [
            "10",
            "CARDINAL"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "para examinar",
            "PERSON"
          ],
          [
            "para manter -se",
            "PERSON"
          ],
          [
            "juntamente",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "altura da liderança",
            "PERSON"
          ],
          [
            "aquela",
            "PERSON"
          ],
          [
            "para se pensar melhor",
            "PERSON"
          ],
          [
            "da própria ganância",
            "PERSON"
          ]
        ],
        "readability_score": 80.65449438202248,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 118,
        "lexical_diversity": 0.6629213483146067
      },
      "preservation_score": 1.21589851458711e-05
    },
    {
      "id": 1,
      "text": "nos faz agir com as nossas emoções, as mesmas emoções que nos \\ncausam danos irreparáveis. Quando os ânimos estão mais frios, \\nos danos já foram causados e eles causam danos e histeria dentro \\nda pró pria família. Assim, não se limitam a aquelas pequenas \\nhisterias, logo as mesmas histerias se transformam na decadência \\nda própria liderança, pois aqueles que não compreendem a sua \\nincapacidade, histerias e falhas indicam a deficiência em não \\nentender sua decadência.    \\nAquele líder que não enxerga seus erros dentro dos \\ninstintos primitivos, que muitos não percebem o tamanho da \\nausência, transformam esse cenário em uma grande histeria \\nmental. Logo, eu vejo que o tamanho de uma liderança está \\nassociado ao po der de um líder em controlar a sua própria histeria, \\npois o líder que chega a uma grande liderança precisa controlar a \\nsi próprio.",
      "position": 48520,
      "chapter": 2,
      "page": 45,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 30.406474820143885,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 27.8,
        "avg_word_length": 5.0215827338129495,
        "unique_word_ratio": 0.6546762589928058,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.1079136690647482,
        "line_break_count": 14,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "danos",
          "histeria",
          "histerias",
          "liderança",
          "líder",
          "emoções",
          "mesmas",
          "causam",
          "dentro",
          "logo",
          "transformam",
          "decadência",
          "própria",
          "pois",
          "tamanho",
          "grande",
          "controlar",
          "agir",
          "nossas",
          "irreparáveis"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "nossas emoções",
            "PERSON"
          ],
          [
            "mesmas emoções",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "ânimos estão mais frios",
            "PERSON"
          ],
          [
            "pria",
            "GPE"
          ],
          [
            "mesmas histerias",
            "PERSON"
          ],
          [
            "decadência \\nda própria",
            "PERSON"
          ],
          [
            "Aquele",
            "ORG"
          ],
          [
            "erros",
            "NORP"
          ]
        ],
        "readability_score": 84.59352517985612,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 91,
        "lexical_diversity": 0.6546762589928058
      },
      "preservation_score": 7.90522254065923e-06
    },
    {
      "id": 1,
      "text": "Capítulo 11   \\nOs miseráveis religiosos   \\nAgora abordaremos as principais dificuldades para liderar \\nos religiosos, eles são sustentados pelas ordens estabelecidas pela \\nprópria religião que foi gerada devido à necessidade de sermos \\ndirecionados e doutrinados em nossas pró prias histerias. Essas \\nhisterias variam de local para local e são as mesmas histerias \\nsemelhantes ao direcionamento religioso de caos vivido em \\nsemelhança ao caos territorial. Logo, percebemos que o líder para \\nos miseráveis religiosos é um líder benevolent e ao erro dos \\nmesmos miseráveis.   \\n “A falsa bondade religiosa é o massacre dos miseráveis...”    \\nAssim, o “líder” religioso não lidera através da sua \\nliderança, e sim através de uma liderança divina, a mesma \\nliderança divina que foi feita para liderar em outro tempo vivido, \\nnão com o caos existente hoje, que é totalmente diferente do caos \\nque se vivia  na Palestina (judeus, Sodoma e Gomorra), índia \\n(budismo, viver com o mínimo possível), filosofia (Grécia, viver \\ncom o luxo), macumba (África, alegria na dor) e muitas outras",
      "position": 49507,
      "chapter": 11,
      "page": 46,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 33.026993865030676,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 32.6,
        "avg_word_length": 5.423312883435583,
        "unique_word_ratio": 0.7055214723926381,
        "avg_paragraph_length": 163.0,
        "punctuation_density": 0.12269938650306748,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "caos",
          "religiosos",
          "histerias",
          "líder",
          "liderança",
          "liderar",
          "local",
          "religioso",
          "vivido",
          "através",
          "divina",
          "viver",
          "capítulo",
          "agora",
          "abordaremos",
          "principais",
          "dificuldades",
          "eles",
          "sustentados"
        ],
        "entities": [
          [
            "11",
            "CARDINAL"
          ],
          [
            "Agora",
            "PERSON"
          ],
          [
            "para liderar \\n",
            "PERSON"
          ],
          [
            "estabelecidas pela",
            "PRODUCT"
          ],
          [
            "própria religião que",
            "ORG"
          ],
          [
            "variam de local",
            "PERSON"
          ],
          [
            "mesmas histerias",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "para \\n",
            "PERSON"
          ],
          [
            "mesmos miseráveis",
            "PERSON"
          ]
        ],
        "readability_score": 82.07300613496932,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 115,
        "lexical_diversity": 0.7055214723926381
      },
      "preservation_score": 2.168289611152246e-05
    },
    {
      "id": 1,
      "text": "religiões que eu não saberei citar todas, mas independente de qual \\nreligião se é seguida hoje em dia, nenhuma delas aceita outra \\nreligião dentro dos seus templos. Assim, o respeito pela divindade \\né o direcionamento para a falta de respeito entre os miseráveis \\nreligiosos. Logo, percebemos que liderar esses miseráveis que se \\nidentificam com as dores religiosas seguidas pelos mesmos \\nmiseráveis que vivem semelhantes àquela idolatria religiosa \\ndirecionada é um processo que merece destaque. Assim, \\npercebemos que é impossível conseguir liderar aqueles que \\nseguem uma religião como regra de vida .   \\n“A miséria é a alavanca da igreja pela falta de viver bem e a \\nsemelhança com o caos de um viver ruim.”   \\nOs miseráveis  religiosos, por  não conseguirem ser \\nliderados e não se preocuparem, não pensam em outros fora do \\nseu ciclo e nem se separam uns d os outros, somente esses \\nmiseráveis são satisfeitos dessa forma, pois sentem uma falsa \\nsegurança e felicidade no caos territorial e mental em que vivem, \\njá que o caos que os levou até a religião é o mesmo que não os faz \\nviver  feliz e seguro. Então, logo p ercebemos que a felicidade de \\num miserável religioso é uma pequena fração de felicidade, pois",
      "position": 50737,
      "chapter": 2,
      "page": 47,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.90035360678925,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.857142857142858,
        "avg_word_length": 4.905940594059406,
        "unique_word_ratio": 0.6386138613861386,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.0891089108910891,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "religião",
          "viver",
          "caos",
          "felicidade",
          "assim",
          "respeito",
          "pela",
          "falta",
          "religiosos",
          "logo",
          "percebemos",
          "liderar",
          "esses",
          "vivem",
          "outros",
          "pois",
          "religiões",
          "saberei",
          "citar"
        ],
        "entities": [
          [
            "religiões que eu não",
            "PERSON"
          ],
          [
            "todas",
            "PERSON"
          ],
          [
            "mas independente de qual",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "outra",
            "CARDINAL"
          ],
          [
            "respeito pela divindade",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "pelos mesmos \\nmiseráveis",
            "PERSON"
          ],
          [
            "àquela idolatria religiosa \\ndirecionada",
            "ORG"
          ]
        ],
        "readability_score": 84.09964639321075,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 129,
        "lexical_diversity": 0.6386138613861386
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "aquela felicidade não pode ser vivida, já que a regra religiosa \\norienta que essa felicidade é errada. Assim, isso transforma a \\nreligião necessária para aquele mis erável religioso, pois sem o \\ncontrole religioso se perdem na fome. Quando isso ocorre na \\nfome cria -se caos, o mesmo caos que mata, rouba, assassina, \\nestupra, engana e todos os erros dignos de ser erros.   \\nVejamos, agora, o lado financeiro religioso.  Aquel es que \\nsabem usar esse aspecto a seu favor tornam -se “grandes líderes”, \\npois a fortuna da igreja vem através da falta de controle das \\nhisterias dos miseráveis. Como mencionado acima, o efeito fã na \\nigreja é o controle, logo, esse controle em uma maior quan tidade \\nde miseráveis religiosos torna -se de “grão em grão a galinha \\nenche o papo”. Assim, a religião teve um crescimento não só de \\nconfiança, mas também monetário acima de qualquer cálculo \\nprevisto, pois ganhos não precisam ser declarados por serem \\ndoação.  Essa doação, por sua vez, muitas vezes é obrigatória, já \\nque os humanos acreditam que estão fazendo o bem para outros \\nmiseráveis religiosos mais miseráveis. Logo, caso se recusem, são \\ntaxados de egoístas e ser egoísta é imoral para qualquer religião.",
      "position": 52071,
      "chapter": 2,
      "page": 48,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 27.495454545454546,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.0,
        "avg_word_length": 4.984848484848484,
        "unique_word_ratio": 0.7121212121212122,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.15656565656565657,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "controle",
          "miseráveis",
          "religião",
          "religioso",
          "pois",
          "felicidade",
          "essa",
          "assim",
          "isso",
          "fome",
          "caos",
          "erros",
          "esse",
          "igreja",
          "acima",
          "logo",
          "religiosos",
          "grão",
          "qualquer",
          "doação"
        ],
        "entities": [
          [
            "aquela felicidade não pode ser vivida",
            "PERSON"
          ],
          [
            "orienta que essa felicidade é errada",
            "ORG"
          ],
          [
            "se perdem",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "rouba",
            "GPE"
          ],
          [
            "assassina",
            "GPE"
          ],
          [
            "erros dignos de ser erros",
            "ORG"
          ],
          [
            "Vejamos",
            "PERSON"
          ],
          [
            "lado financeiro",
            "PERSON"
          ],
          [
            "Aquel",
            "PERSON"
          ]
        ],
        "readability_score": 87.50454545454545,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 141,
        "lexical_diversity": 0.7121212121212122
      },
      "preservation_score": 2.574843913243292e-05
    },
    {
      "id": 1,
      "text": "“Assim, qualquer religião te dará bondade e outras infinitas \\nvirtudes em uma grandeza que  \\na miséria caótica não permitia você ter.”    \\nUm líder territorial do tamanho de um estado, para \\nconseguir o controle populacional, depende de uma grande \\nliderança, as sim como uma grande religião precisa.  Logo, \\nentendemos como todos os miseráveis tiveram uma grande \\nevolução devido ao sentimento do caos ser semelhante à religião \\nde maior força monetária, após “se consolidar” como a maioria \\nterritorial. Assim, os costume s locais se alteram, alterando os \\ncostumes locais, as mesmas alterações ocasionam conflitos \\ndentro e fora da própria religião devido às novas regras serem fora \\nde um costume territorial e à diferença sobre como viver a vida.   \\nGanhar a confiança pelo senti mento é manter um \\nrelacionamento longo, logo nos perguntamos: qual é o valor do \\nmeu sentimento para a religião que me tirou da fome?",
      "position": 53395,
      "chapter": 2,
      "page": 49,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.157931034482758,
      "complexity_metrics": {
        "word_count": 145,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 29.0,
        "avg_word_length": 5.1931034482758625,
        "unique_word_ratio": 0.7310344827586207,
        "avg_paragraph_length": 145.0,
        "punctuation_density": 0.1103448275862069,
        "line_break_count": 15,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "religião",
          "como",
          "territorial",
          "grande",
          "assim",
          "logo",
          "devido",
          "sentimento",
          "costume",
          "locais",
          "fora",
          "qualquer",
          "dará",
          "bondade",
          "outras",
          "infinitas",
          "virtudes",
          "grandeza",
          "miséria",
          "caótica"
        ],
        "entities": [
          [
            "permitia",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "alteram",
            "ORG"
          ],
          [
            "alterando",
            "ORG"
          ],
          [
            "mesmas alterações",
            "PERSON"
          ],
          [
            "fora da própria religião devido",
            "ORG"
          ],
          [
            "novas",
            "GPE"
          ],
          [
            "serem fora \\nde",
            "PERSON"
          ]
        ],
        "readability_score": 83.94206896551724,
        "semantic_density": 0,
        "word_count": 145,
        "unique_words": 106,
        "lexical_diversity": 0.7310344827586207
      },
      "preservation_score": 1.1293175058084614e-05
    },
    {
      "id": 1,
      "text": "Capítulo 12   \\nOs miseráveis agressivos    \\nVenho dizer que esses líderes caóticos são exemplos a \\nserem explorados, pois vêm de uma herança de caos. O mesmo \\ncaos que nos moldou em um viver será o mesmo que vai nos \\nmoldar para um futuro, pois se temos extravagâncias no caos é \\nporque aquele caos tem m uitas diferenças de ser feliz, já que a \\nfelicidade é um termo muito relativo. Assim, a felicidade dos \\nmiseráveis pode ser de matar pessoas a ter medo de uma barata. \\nTodos na vida têm uma forma de enxergar a felicidade relativa ao \\nseu próprio viver, porém t emos padrões e regras exatas e \\nnecessárias para ter um respeito de   \\n“não faço com os outros aquilo que eu não gosto que faça \\ncomigo”. Desse modo, como foi mencionado anteriormente sobre \\na religião, é a mesma forma de pensar igual, porém diferente \\ndaqueles  que não vivem na mesma religião. Então, temos que ter \\numa coerência de aceitar o meu incômodo diante da sua \\nfelicidade, devido a não ocorrer essa observação básica de viver \\nbem um para com o outro, criamos novas tecnologias para não \\nmatarmos uns aos outro s e sempre ocorre o oposto da criação.",
      "position": 54481,
      "chapter": 12,
      "page": 50,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 32.86818181818182,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 33.0,
        "avg_word_length": 4.5606060606060606,
        "unique_word_ratio": 0.6868686868686869,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.08585858585858586,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "felicidade",
          "viver",
          "miseráveis",
          "pois",
          "mesmo",
          "temos",
          "forma",
          "porém",
          "religião",
          "mesma",
          "outro",
          "capítulo",
          "agressivos",
          "venho",
          "dizer",
          "esses",
          "líderes",
          "caóticos",
          "exemplos"
        ],
        "entities": [
          [
            "12",
            "CARDINAL"
          ],
          [
            "agressivos",
            "GPE"
          ],
          [
            "Venho",
            "GPE"
          ],
          [
            "caóticos são",
            "PERSON"
          ],
          [
            "termo muito relativo",
            "ORG"
          ],
          [
            "ser de matar",
            "ORG"
          ],
          [
            "medo de uma barata",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "necessárias",
            "PERSON"
          ],
          [
            "que eu não gosto que faça \\ncomigo",
            "PERSON"
          ]
        ],
        "readability_score": 82.13181818181818,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 136,
        "lexical_diversity": 0.6868686868686869
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "Logo, enxergamos que é impossível não haver esses tipos de \\nmiseráveis agressivos, pois o sistema é totalmente contra a ideia \\nde viver bem entre a miséria, já que a miséria não tem como ser \\nboa. Desse modo, todo miserá vel quer ser rico e, quando todos \\nquerem um mesmo objetivo, conflitos  são gerados, guerras, \\nganâncias, ostentação, egocentrismo e muitas outros sentimentos \\nque vão ser discutidos  neste capítulo.   \\nNão adianta que o líder caótico conquiste um território \\nsem manter os benefícios, mas a dificuldade não está em fazer, e \\nsim saber qual é o benefício diante dos costumes de cada um, \\npois assim como cada um tem as causas de seus momentos de \\nbem-estar  e de ma l-estar, o líder também. Além disso, o trajeto \\ndo líder caótico foi de mentiras, enganação, ocultamento e \\noutras ações necessárias para ser um líder caótico.   \\nAssim como um líder caótico teve a necessidade de ter \\nproblemas, terá a mesma necessidade de cor rigir os mesmos \\nproblemas, assim como os novos e os velhos líderes caóticos \\ncriam regras, os miseráveis caóticos necessitam também da \\nconfiança deles.  Não há como haver boas regras em territórios \\nonde não existe caos e onde existe caos não convêm que haja  boas",
      "position": 55763,
      "chapter": 2,
      "page": 51,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.29620462046205,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 33.666666666666664,
        "avg_word_length": 4.876237623762377,
        "unique_word_ratio": 0.6633663366336634,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.12376237623762376,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "líder",
          "caótico",
          "assim",
          "haver",
          "miseráveis",
          "pois",
          "miséria",
          "cada",
          "também",
          "necessidade",
          "problemas",
          "caóticos",
          "regras",
          "boas",
          "onde",
          "existe",
          "caos",
          "logo",
          "enxergamos"
        ],
        "entities": [
          [
            "Logo",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "caótico conquiste",
            "PERSON"
          ],
          [
            "benefício diante",
            "PERSON"
          ],
          [
            "causas de seus momentos de \\nbem-estar",
            "PERSON"
          ],
          [
            "Além disso",
            "PERSON"
          ],
          [
            "caótico foi de mentiras",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ]
        ],
        "readability_score": 81.70379537953795,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 134,
        "lexical_diversity": 0.6633663366336634
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "regras. Um líder caótico jamais estará firme e seguro, porque \\ntodos os líderes caóticos são desunidos, gananciosos, \\nindisciplinados, infiéis seja qual for a liderança, seja ela religiosa, \\nmonetária, política, fama, dom, amor, guerra, protesto, \\nmanife stação, costumes, os líderes caóticos miseráveis cresceram \\natravés do interesse, por isso não são de confiança.   \\nEsses líderes caóticos são extravagantes e, assim, temos \\ntantos excessos que deixamos de perceber o tamanho da nossa \\nprópria ganância, porque eles sempre aspirarão à própria \\nextravagância. É necessário destacar que alguns miseráveis \\ncaóticos querem ser líderes caóticos e se acham grandes devido à \\nobservação de que o “erro”, muitas vezes, levou alguns à \\nliderança. No entanto, esse mesmo erro será  o seu maior caos.   \\nA vivência do líder caótico e o fato de ser grande dentro \\ndo caos ocorrem devido a sua própria grandeza, já que ele tem um \\nsentimento de ser semelhante aos líderes caóticos secundários.  \\nNão ser líder diante do que te transformou em lí der é o fracasso \\nda própria liderança. Logo, o ser que vivencia situações em que a \\nconquista não ocorreu através da confiança não é confiável.",
      "position": 57093,
      "chapter": 2,
      "page": 52,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.08804347826087,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.0,
        "avg_word_length": 5.293478260869565,
        "unique_word_ratio": 0.6793478260869565,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.17391304347826086,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caóticos",
          "líderes",
          "própria",
          "líder",
          "liderança",
          "caótico",
          "porque",
          "seja",
          "miseráveis",
          "através",
          "confiança",
          "alguns",
          "devido",
          "erro",
          "caos",
          "regras",
          "jamais",
          "estará",
          "firme",
          "seguro"
        ],
        "entities": [
          [
            "caótico jamais estará",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "caóticos",
            "GPE"
          ],
          [
            "ela religiosa",
            "PERSON"
          ],
          [
            "monetária",
            "PERSON"
          ],
          [
            "caóticos miseráveis",
            "PERSON"
          ],
          [
            "caóticos são",
            "PERSON"
          ],
          [
            "deixamos de perceber",
            "ORG"
          ],
          [
            "própria ganância",
            "PERSON"
          ],
          [
            "própria \\nextravagância",
            "PERSON"
          ]
        ],
        "readability_score": 86.91195652173913,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 125,
        "lexical_diversity": 0.6793478260869565
      },
      "preservation_score": 2.303807711849261e-05
    },
    {
      "id": 1,
      "text": "Temos os líderes caóticos pelo caos do amor ser \\nsemelhante à vida caótica de seus liderados. Esses líderes, par a \\ncriarem um sentimento de amor dentro do caos, geralmente vêm \\ndentro de uma religião ou sentimento de um viver em caos \\nsemelhante (favela com tráfico, milícias). Para se manter esse tipo \\nde liderança tem que ser muito convicto de suas ações dignas de \\nserem erradas, pois essas ações têm um valor coletivo sentimental \\nmaior que a sua necessidade, até porque cada um  enxerga  a sua \\nforma de viver a vida como a certa para o mundo.    \\nLogo, o meu erro tem um sentimento semelhante  à \\nnecessidade  territorial  ou religiosa em que ele é \\nnecessário. Manter a liderança caótica quando se perde o \\nsentimento só recupera o que se tem mais valor sentimental, \\naquele mesmo que foi o seu erro necessário para ser líder, é \\nnecessário sempre fazer, pois o desespero de manter uma vida \\nfaz muitos desistirem do próprio sentimento que o fez ter a \\nconfiança daqueles miseráveis caóticos. Esses miseráveis, \\nquando ganham a confiança através de um interesse, não \\nsustentam a confiança devido à forma de viver fazer o seu \\npróprio viver. Temos  líderes caóticos devido aos miseráveis \\ncaóticos do seu entorno serem muito miseráveis para evoluir",
      "position": 58392,
      "chapter": 2,
      "page": 53,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.392239010989012,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.714285714285715,
        "avg_word_length": 4.908653846153846,
        "unique_word_ratio": 0.5625,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.08173076923076923,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sentimento",
          "caóticos",
          "viver",
          "miseráveis",
          "líderes",
          "caos",
          "semelhante",
          "vida",
          "manter",
          "necessário",
          "confiança",
          "temos",
          "amor",
          "caótica",
          "esses",
          "dentro",
          "liderança",
          "muito",
          "ações",
          "serem"
        ],
        "entities": [
          [
            "caóticos pelo",
            "PERSON"
          ],
          [
            "Para se manter",
            "PERSON"
          ],
          [
            "muito convicto de suas",
            "PERSON"
          ],
          [
            "ações dignas de \\nserem erradas",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "Manter",
            "PERSON"
          ],
          [
            "quando se perde",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para ser líder",
            "PRODUCT"
          ]
        ],
        "readability_score": 83.67026098901098,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 117,
        "lexical_diversity": 0.5625
      },
      "preservation_score": 1.4304688406907178e-05
    },
    {
      "id": 1,
      "text": "junto com eles. O peso por buscar nossas conquistas não pode \\nser colocado somente em um líder caótico, e sim em todo um \\ncontexto territorial e de confiança.    \\nO líder caótico com “grande massa” não consegue \\nadministrar a felicidade e a tristeza a partir de onde lidera, pois \\nsem o caos nesse território não haverá paz, já que a paz e o caos \\nde cada sujeito são diferentes dos costumes e de suas \\ninterpretações. A ssim como amor e ódio são as “mesmas coisas”, \\na felicidade e a tristeza têm que ser balanceada de acordo com o \\ncaos territorial, ambas para manter -se em equilíbrio. Logo, \\nentendemos que manter uma liderança caótica para si próprio não \\né possível, pois são muitos sentimentos sem confiança para \\nequilibrar.   \\nAqueles líderes caóticos que lideram através da guerra e \\ndo ódio ganham a confiança daqueles miseráveis odiosos, aqueles \\nque quando perdem a confiança conquistada através do ódio, \\natravés de um ódio maior  vão cobrar... Qualquer “confiança” \\nconquistada através do monetário também pode se perder por um \\nvalor maior. Assim, muitos se tornam prisioneiros uns dos outros \\ne precisam se libertar sem resgate, pois aquelas ações de guerra",
      "position": 59765,
      "chapter": 2,
      "page": 54,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.550064766839377,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 24.125,
        "avg_word_length": 4.958549222797927,
        "unique_word_ratio": 0.6373056994818653,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.10362694300518134,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "confiança",
          "ódio",
          "através",
          "pois",
          "caos",
          "pode",
          "líder",
          "caótico",
          "territorial",
          "felicidade",
          "tristeza",
          "manter",
          "muitos",
          "aqueles",
          "guerra",
          "conquistada",
          "maior",
          "junto",
          "eles",
          "peso"
        ],
        "entities": [
          [
            "balanceada de acordo",
            "ORG"
          ],
          [
            "para manter",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "Aqueles",
            "PERSON"
          ],
          [
            "caóticos",
            "GPE"
          ],
          [
            "que quando perdem",
            "PERSON"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "Qualquer",
            "PERSON"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "monetário também pode se",
            "PERSON"
          ]
        ],
        "readability_score": 86.44993523316062,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 123,
        "lexical_diversity": 0.6373056994818653
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "não têm volta. Essas ações q ue, inicialmente, trazem felicidade, \\ntambém trazem morte, por não conseguirem limitar as ações do \\nseu entorno.  Ela não consegue ser limitada devido ao limite ser  a \\nmorte!!",
      "position": 61055,
      "chapter": 2,
      "page": 55,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.027272727272727,
      "complexity_metrics": {
        "word_count": 33,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 11.0,
        "avg_word_length": 5.090909090909091,
        "unique_word_ratio": 0.8484848484848485,
        "avg_paragraph_length": 33.0,
        "punctuation_density": 0.24242424242424243,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ações",
          "trazem",
          "morte",
          "volta",
          "essas",
          "inicialmente",
          "felicidade",
          "também",
          "conseguirem",
          "limitar",
          "entorno",
          "consegue",
          "limitada",
          "devido",
          "limite"
        ],
        "entities": [
          [
            "não têm volta",
            "ORG"
          ],
          [
            "Essas",
            "GPE"
          ],
          [
            "também trazem morte",
            "ORG"
          ],
          [
            "Ela",
            "PERSON"
          ],
          [
            "limitada devido",
            "PERSON"
          ],
          [
            "limite ser",
            "PERSON"
          ]
        ],
        "readability_score": 92.97272727272727,
        "semantic_density": 0,
        "word_count": 33,
        "unique_words": 28,
        "lexical_diversity": 0.8484848484848485
      },
      "preservation_score": 9.03454004646769e-07
    },
    {
      "id": 1,
      "text": "Capítulo 13   \\nOs miseráveis caóticos   \\nÉ fato que nem todos vão conseguir “ser grandes” ou \\nfortes o suficiente para a grandeza, mas aqueles que \\ncomplementam a sociedade são os que intermediam a miséria e a \\nluxúria. Esses são miseráveis que vivem em caos, pois precisam \\nsempre pensar na fome e, a lém disso, são aqueles chamados de \\nclasse média. É necessário observar que se pode ganhar um \\nmilhão e ter um custo para gastar 1 milhão, os mesmos um milhão \\nou um pouco menos, ou aqueles que sabem sobreviver com 5 mil, \\nindependentemente do valor que ganhar am.  Pensar na fome não \\nnos permite evoluir o que nós humanos poderíamos evoluir. \\nAquele que ganha 1 milhão vive na miséria luxuosa e aquele que \\nganha 5 mil vive na miséria confortável, ambos podem ser felizes \\nou tristes, mas nunca irão deixar de viver sen do miseráveis \\ncaóticos.   \\nEsses miseráveis caóticos não são sábios ou inteligentes, \\na falta de sabedoria ou inteligência de si próprio os deixa \\npequenos diante da liderança e grandes diante da pobreza. Logo, \\né importante que o líder saiba quais miseráveis caóticos são os",
      "position": 61404,
      "chapter": 13,
      "page": 56,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.719585253456223,
      "complexity_metrics": {
        "word_count": 186,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 26.571428571428573,
        "avg_word_length": 4.779569892473118,
        "unique_word_ratio": 0.6397849462365591,
        "avg_paragraph_length": 186.0,
        "punctuation_density": 0.0913978494623656,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "caóticos",
          "milhão",
          "aqueles",
          "miséria",
          "grandes",
          "esses",
          "pensar",
          "fome",
          "ganhar",
          "evoluir",
          "aquele",
          "ganha",
          "vive",
          "diante",
          "capítulo",
          "fato",
          "todos",
          "conseguir",
          "fortes"
        ],
        "entities": [
          [
            "13",
            "CARDINAL"
          ],
          [
            "caóticos   \\n",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "1 milhão",
            "MONEY"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "Pensar",
            "PERSON"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "ambos podem",
            "PERSON"
          ]
        ],
        "readability_score": 85.28041474654378,
        "semantic_density": 0,
        "word_count": 186,
        "unique_words": 119,
        "lexical_diversity": 0.6397849462365591
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "liderados de caráter comum, pois eles trazem felicidades, \\ntristezas, amor e tudo o que é frequente na vida de um líder com \\nmuitos miseráveis caóticos, pois esses miseráveis caóticos são \\naqueles que mais trabalham para viver em sua miséria s atisfatória. \\nEsses são aqueles que, quando se tem a confiança, vão oferecer \\nmais do que outros miseráveis, pois são satisfeitos em estar no \\nmeio, estar na mediocridade satisfatória de viver, em ter uma \\ncasa, uma cama, um filho na escola, ter a necessidade básica \\nconfortável para um viver digno. Porém, esse viver digno o faz \\nnão viver o sentimento dos seus sacrifícios, pois os mesmos \\nsacrifícios feitos para viver essa vida medíocre são os mesmos \\nque não permitem que tenhamos tempo para viver as nossas \\nconqui stas, já que não se tem tempo para viver com a sua família \\ne com seus amigos e isso contribui para que seja um miserável \\ncaótico.   \\n“Aquele miserável caótico pelo monetário através do excesso \\npara si próprio é a ruína  da sua própria organização monetária.”   \\nA pouca prudência dos miseráveis caóticos muitas vezes \\nfaz com que iniciem algo que parece bom, sem perceber a questão \\ncentral qu e isso encobre, isso ocorre não por um erro, e sim por",
      "position": 62650,
      "chapter": 2,
      "page": 57,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.44731707317073,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 41.0,
        "avg_word_length": 4.824390243902439,
        "unique_word_ratio": 0.624390243902439,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.1073170731707317,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "pois",
          "miseráveis",
          "caóticos",
          "isso",
          "vida",
          "esses",
          "aqueles",
          "mais",
          "digno",
          "seus",
          "sacrifícios",
          "mesmos",
          "tempo",
          "miserável",
          "caótico",
          "liderados",
          "caráter",
          "comum",
          "eles"
        ],
        "entities": [
          [
            "miseráveis caóticos",
            "PERSON"
          ],
          [
            "caóticos são \\naqueles",
            "PERSON"
          ],
          [
            "trabalham para",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "que outros miseráveis",
            "ORG"
          ],
          [
            "básica",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "mesmos \\nque",
            "PERSON"
          ],
          [
            "caótico pelo monetário através",
            "PERSON"
          ],
          [
            "monetária",
            "PERSON"
          ]
        ],
        "readability_score": 78.05268292682928,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 128,
        "lexical_diversity": 0.624390243902439
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "não ser inteligente para perceber que está vivendo de acordo com \\na típica frase popular “Maria vai com as outras”.  Devido a ter \\nfome e não perceber que está adaptado a ter pequena ganância \\nproporciona l a si próprio, isso o faz ter erros de grande proporção \\ne pequenos valores ganhos, muitas vezes não ganhando e só \\nperdendo, mas a sua falta de sabedoria e inteligência o faz pensar \\nque aquele erro seria de bom ganho. Por muitas vezes, esse erro \\nvem do pen samento de que a solução para organizar esse excesso \\nde capitalismo gera mais capitalismo, que foi gerado devido à \\nadmiração pelos líderes caóticos, a mesma admiração gerada pelo \\nnosso próprio capitalismo.   \\nJá aqueles líderes caóticos não veem necessidade  de \\nmelhorar os miseráveis caóticos, observamos que não querer \\nmelhorar da miséria é uma estratégia de se fazer a economia de \\num país. Como dito acima, independentemente de onde o \\nmiserável caótico esteja, seja no monetário, seja na confiança, \\nambas as nec essidades são movimentadas por esses miseráveis.   \\nOs miseráveis caóticos são tão importantes quanto um \\nlíder, porém um líder apresenta mais poder que um miserável \\ncaótico. O mesmo que se movimenta entre todas as classes sociais",
      "position": 63983,
      "chapter": 2,
      "page": 58,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.7173007896626,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.428571428571427,
        "avg_word_length": 5.010050251256281,
        "unique_word_ratio": 0.7085427135678392,
        "avg_paragraph_length": 199.0,
        "punctuation_density": 0.09045226130653267,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caóticos",
          "capitalismo",
          "miseráveis",
          "perceber",
          "está",
          "devido",
          "próprio",
          "muitas",
          "vezes",
          "erro",
          "esse",
          "mais",
          "admiração",
          "líderes",
          "melhorar",
          "miserável",
          "caótico",
          "seja",
          "líder",
          "inteligente"
        ],
        "entities": [
          [
            "não ser inteligente",
            "PERSON"
          ],
          [
            "para perceber",
            "PERSON"
          ],
          [
            "Maria",
            "NORP"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "gera mais capitalismo",
            "PERSON"
          ],
          [
            "admiração pelos",
            "PERSON"
          ],
          [
            "caóticos",
            "GPE"
          ],
          [
            "gerada pelo \\nnosso",
            "PERSON"
          ]
        ],
        "readability_score": 84.2826992103374,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 141,
        "lexical_diversity": 0.7085427135678392
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "e todos os territórios e é  aquele que simpatiza com o líder e o \\nsegue fazendo uma grande “network” a favor do líder. Eles \\nmostram tanta determinação que às vezes parecem que seriam \\nbons líderes. No entanto, quando se é dada a chance de ser líder, \\nmaior será a cobrança, pois como o líder chegou à liderança pela \\nadmiração dos miseráveis, como o novo líder conseguirá obter a \\nadmiração semelhante à do antigo líder?    \\nA necessidade do miserável caótico de seguir um padrão \\nsocial gera caos devido à falta de compreensão do outro miserável  \\ncaótico. Logo, o miserável caótico, quando se transforma em um \\nlíder, tem interferências do seu padrão social, que não os faz ser \\num líder melhor. Uma alternativa possível para mudar esse \\ncenário é possível se ele conseguir aprender a usar a sua miséria \\na seu favor. Assim, o miserável caótico consegue ser um líder \\nmelhor do que o anterior.",
      "position": 65319,
      "chapter": 2,
      "page": 59,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.35014005602241,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 21.857142857142858,
        "avg_word_length": 4.738562091503268,
        "unique_word_ratio": 0.6601307189542484,
        "avg_paragraph_length": 153.0,
        "punctuation_density": 0.10457516339869281,
        "line_break_count": 14,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "miserável",
          "caótico",
          "favor",
          "quando",
          "como",
          "admiração",
          "padrão",
          "social",
          "melhor",
          "possível",
          "todos",
          "territórios",
          "aquele",
          "simpatiza",
          "segue",
          "fazendo",
          "grande",
          "network",
          "eles"
        ],
        "entities": [
          [
            "seriam",
            "GPE"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "novo líder",
            "PERSON"
          ],
          [
            "miserável caótico de seguir",
            "PERSON"
          ],
          [
            "falta de compreensão",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "miserável caótico",
            "GPE"
          ],
          [
            "quando se transforma",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 87.64985994397759,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 101,
        "lexical_diversity": 0.6601307189542484
      },
      "preservation_score": 9.486267048791075e-06
    },
    {
      "id": 1,
      "text": "Capítulo 14   \\nLíderes políticos   \\nPrimeiro precisamos saber acerca da maior dificuldade em \\nser político em qualquer tempo vivido por nós miseráveis. Essa \\ndificuldade sendo resolvida será uma solução provisória para \\nnovas dificuldades, mesmo que seja a extinção da fome, não \\nadiantará se não  tiver confiança, organização e disciplina, pois \\nessa é a única arte que compete a quem comanda. Caso não seja, \\npodemos pensar que a fome nunca será extinta e, em uma \\nhierarquia monetária, é necessário obter um estímulo de um viver \\npossível na miséria. A m esma miséria que serve para evoluir \\ndaqueles que querem usufruir do luxo não consegue beneficiar o \\nlado mais incomodado com algo que faça o outro lado mais feliz.    \\nUm miserável político que se ausenta nas dificuldades não \\nera para estar nessa posição, o miserável político deve estar \\nsempre entre os miseráveis para acostumar o corpo e a mente, em \\nparte, para conhecer a natureza dos lugares e saber como ganhar \\na confiança entre os miseráveis. Até para ser um bom miserável \\npolítico a liderança não vem com a bondade, assim como não há \\nliderança sendo ruim, ter entendimento sobre si próprio é a opção",
      "position": 66349,
      "chapter": 14,
      "page": 60,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 32.4890625,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.0,
        "avg_word_length": 4.963541666666667,
        "unique_word_ratio": 0.6875,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.08854166666666667,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "político",
          "miseráveis",
          "miserável",
          "saber",
          "dificuldade",
          "essa",
          "sendo",
          "será",
          "dificuldades",
          "seja",
          "fome",
          "confiança",
          "miséria",
          "lado",
          "mais",
          "entre",
          "como",
          "liderança",
          "capítulo",
          "líderes"
        ],
        "entities": [
          [
            "14",
            "CARDINAL"
          ],
          [
            "Primeiro",
            "ORG"
          ],
          [
            "vivido por nós miseráveis",
            "ORG"
          ],
          [
            "disciplina",
            "GPE"
          ],
          [
            "hierarquia monetária",
            "PERSON"
          ],
          [
            "daqueles",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "lado mais",
            "PERSON"
          ],
          [
            "outro lado mais",
            "PERSON"
          ],
          [
            "para acostumar",
            "PERSON"
          ]
        ],
        "readability_score": 82.5109375,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 132,
        "lexical_diversity": 0.6875
      },
      "preservation_score": 1.21589851458711e-05
    },
    {
      "id": 1,
      "text": "a ser seguida quando se tem dúvidas do que é certo, pois as \\nescolhas orientam para que seja um líder político.    \\nOs nossos costumes vêm de um padrão vivido por ou tros \\ne evoluído por nós mesmos. Um miserável político inteligente \\ndeve ser sábio e observar as semelhanças de como proceder, \\nnunca ficando ocioso nos tempos de paz, mas sim com habilidade \\npara saber utilizar a confiança conquistada na adversidade, pois \\nquando mudar para tempos de caos deve estar preparado para \\nresistir.  Conhecer os costumes locais nos faz entender a \\nsemelhança do caos um para com o outro, ensinando -nos a maior \\nimportância da totalidade, em que há costumes diferentes e \\ntempos diferentes.   \\nA criação de líderes políticos caóticos ocorre devido a não \\nentenderem e compreenderem a evolução do comportamento, por \\nnão terem vivido na mesma época, “pois o sentimento do tempo \\nem que está sendo um líder político para os miseráveis não é de \\ncomum e aco rdo com os miseráveis.”   \\nUm bom líder não é aquele que beneficia os mais velhos, \\npois sendo mais velhos já viveram uma vida cheia de miseráveis \\ncom os erros políticos semelhantes, não por querer errar, e sim",
      "position": 67673,
      "chapter": 3,
      "page": 61,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.77948717948718,
      "complexity_metrics": {
        "word_count": 195,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.5,
        "avg_word_length": 4.82051282051282,
        "unique_word_ratio": 0.6307692307692307,
        "avg_paragraph_length": 195.0,
        "punctuation_density": 0.08205128205128205,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "líder",
          "político",
          "costumes",
          "tempos",
          "miseráveis",
          "quando",
          "vivido",
          "deve",
          "caos",
          "diferentes",
          "políticos",
          "sendo",
          "mais",
          "velhos",
          "seguida",
          "dúvidas",
          "certo",
          "escolhas",
          "orientam"
        ],
        "entities": [
          [
            "quando se",
            "PERSON"
          ],
          [
            "político",
            "PERSON"
          ],
          [
            "semelhanças de como proceder",
            "ORG"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "para tempos de caos deve estar",
            "PERSON"
          ],
          [
            "para \\nresistir",
            "PERSON"
          ],
          [
            "Conhecer",
            "PRODUCT"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "políticos caóticos",
            "PERSON"
          ],
          [
            "não terem vivido",
            "PERSON"
          ]
        ],
        "readability_score": 82.30384615384615,
        "semantic_density": 0,
        "word_count": 195,
        "unique_words": 123,
        "lexical_diversity": 0.6307692307692307
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "pela necessidade de errar para ser um miserável  político. Logo, \\nenxergamos um outro agravante para aqueles velhos líderes \\nmiseráveis: são esses quem têm mais dinheiro, que são mais \\nbeneficiados, por isso não deveriam ser mais beneficiados que os \\njovens. Eles deveriam receber para guiar os mais jovens, viver \\ncom menos luxo e viver uma vida mais tranquila e confortável, \\npois estão mais próximos da morte, logo não vejo necessidade de \\nse ter vivido toda uma vida de luxo e morrer no luxo, já que o \\npróprio luxo poderia ajudar aos miseráveis a não serem \\nmiserá veis.   \\nVejo que é impossível acontecer isso na política, pois a \\nmesma política em que os mais velhos deveriam ensinar é aquela \\nque eles roubam, assassinam, destroem e consomem tudo o que é \\ndesnecessário devido ao próprio pensamento arcaico de um estilo \\nde vida totalmente diferente daquele que precisamos para viver e \\naceitar uns aos outros. Todos esses velhos miseráveis políticos \\ndesconhecem o motivo da conquista de estar na liderança, pois \\nnão viveram o caos em que os novos miseráveis vivem. Logo, não \\nsaberão liderar os miseráveis da mesma forma, não saberão os \\ncostumes territoriais, transformando -se, assim, em um líder que \\nnão sabe liderar, já que não há concordância com os miseráveis.",
      "position": 68950,
      "chapter": 3,
      "page": 62,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.84487179487179,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.666666666666664,
        "avg_word_length": 5.038461538461538,
        "unique_word_ratio": 0.6009615384615384,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.11538461538461539,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "miseráveis",
          "luxo",
          "logo",
          "velhos",
          "deveriam",
          "viver",
          "vida",
          "pois",
          "necessidade",
          "esses",
          "beneficiados",
          "isso",
          "jovens",
          "eles",
          "vejo",
          "próprio",
          "política",
          "mesma",
          "saberão"
        ],
        "entities": [
          [
            "pela necessidade de errar",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "outro",
            "ORG"
          ],
          [
            "quem têm mais dinheiro",
            "ORG"
          ],
          [
            "deveriam ser mais",
            "PERSON"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "Vejo",
            "PERSON"
          ],
          [
            "deveriam ensinar",
            "PERSON"
          ],
          [
            "aquela \\nque",
            "PERSON"
          ],
          [
            "consomem tudo o que",
            "ORG"
          ]
        ],
        "readability_score": 81.15512820512821,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 125,
        "lexical_diversity": 0.6009615384615384
      },
      "preservation_score": 1.8821958430141022e-05
    },
    {
      "id": 1,
      "text": "Capítulo 15   \\n De miserável para político miserável   \\nResta ver, agora, quais devem ser os modos de um \\nmiserável político agir para os miseráveis e para aqueles \\nmiseráveis amigos que, como mencionado em capítulos \\nanteriores, buscam a verdade extraída dos fatos e não dá \\nimaginação. A falta de incoerência a um padrão dos fatos \\ncomportamentais diante de uma verdade de um maior contexto \\nnos faz ser benevolentes a um padrão errado que se torna certo. \\nHá diferença entre os miseráveis sobre como se vive e como se \\ndeveria viver, pois aquele que abandona o que se faz p or aquilo \\nque se deveria fazer aprenderá que abandonar a sua própria \\ntrajetória o faz perder -se na liderança, não por querer abandonar, \\ne sim por cair nas próprias tentações do trajeto. Não saber limitar \\nas tentações é um dos erros que pode levar à perda d a liderança, \\npois através desse erro um político miserável bom se perderá em \\nmeio a tantos que não são bons. Como também foi mencionado \\nantes, um líder político não provém de muitas felicidades que \\npossa se ter um julgamento ruim, uns vão admirar e outros vão",
      "position": 70514,
      "chapter": 15,
      "page": 64,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.40526315789474,
      "complexity_metrics": {
        "word_count": 190,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 38.0,
        "avg_word_length": 4.684210526315789,
        "unique_word_ratio": 0.6473684210526316,
        "avg_paragraph_length": 190.0,
        "punctuation_density": 0.07368421052631578,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miserável",
          "político",
          "como",
          "miseráveis",
          "mencionado",
          "verdade",
          "fatos",
          "padrão",
          "deveria",
          "pois",
          "abandonar",
          "liderança",
          "tentações",
          "capítulo",
          "resta",
          "agora",
          "quais",
          "devem",
          "modos",
          "agir"
        ],
        "entities": [
          [
            "Resta",
            "ORG"
          ],
          [
            "agora",
            "GPE"
          ],
          [
            "devem ser",
            "PERSON"
          ],
          [
            "político agir para",
            "PRODUCT"
          ],
          [
            "diante de uma verdade de",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "se torna",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "aprenderá que",
            "PERSON"
          ]
        ],
        "readability_score": 79.59473684210526,
        "semantic_density": 0,
        "word_count": 190,
        "unique_words": 123,
        "lexical_diversity": 0.6473684210526316
      },
      "preservation_score": 1.0163857552276153e-05
    },
    {
      "id": 1,
      "text": "criticar. Logo, é necessário notar que alguns “acarretam” \\nconfiança, enquanto outros vão trazer caos .   \\nUm líder político miserável não pode ter a luxúria de \\nalgum “vício”, pois essas fugas infames para aqueles miseráveis \\n“tradicionais” os fariam perd er o poder, pois um grande líder \\npolítico miserável não é aquele que segue a ganância do poder, e \\nsim aquele que segue a maior quantidade de um contexto \\nsentimental.    \\nIsso porque aquele trajeto da miséria até a liderança \\npolítica o fez viver muitos vícios que, sem eles, seria difícil \\nconseguir ter forças para viver. Os mesmos vícios que deram \\nforça para aguentar o trajeto são aqueles que colocam em risco a \\nsua liderança ; pois se bem considerado for tudo, sempre se \\nencontrará uma regra que parece certa, porém aquela regra que \\nparece certa para alguns, para outros será incômodo e eles \\nincomodados  poderão dar origem a outras regras que incomodam \\na outros incomodados.",
      "position": 71769,
      "chapter": 3,
      "page": 65,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.711764705882352,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 30.6,
        "avg_word_length": 5.03921568627451,
        "unique_word_ratio": 0.7189542483660131,
        "avg_paragraph_length": 153.0,
        "punctuation_density": 0.10457516339869281,
        "line_break_count": 16,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "outros",
          "pois",
          "aquele",
          "alguns",
          "líder",
          "político",
          "miserável",
          "aqueles",
          "poder",
          "segue",
          "trajeto",
          "liderança",
          "viver",
          "vícios",
          "eles",
          "regra",
          "parece",
          "certa",
          "incomodados",
          "criticar"
        ],
        "entities": [
          [
            "necessário notar que",
            "ORG"
          ],
          [
            "confiança",
            "GPE"
          ],
          [
            "pois essas fugas",
            "ORG"
          ],
          [
            "para aqueles miseráveis",
            "PERSON"
          ],
          [
            "Isso",
            "PERSON"
          ],
          [
            "seria difícil \\nconseguir",
            "ORG"
          ],
          [
            "forças",
            "ORG"
          ],
          [
            "aquela",
            "PERSON"
          ],
          [
            "certa",
            "NORP"
          ],
          [
            "para outros será",
            "PERSON"
          ]
        ],
        "readability_score": 83.18823529411765,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 110,
        "lexical_diversity": 0.7189542483660131
      },
      "preservation_score": 1.325065873481928e-05
    },
    {
      "id": 1,
      "text": "Capítulo 16  \\n Liberdade?   \\nA liberdade, quando usada de uma forma que se torne \\nconhecida por todos, te prejudica, pois nem todos podem ser \\nbenevolentes e ter liberdade, já que através da liberdade em \\nexcesso pode -se ocorrer que o viver de um líder seja o sentimento \\nde propagação daq ueles que estão sendo liderados. Logo, percebo \\nque dar liberdade para aqueles que não conquistam a confiança \\natravés do sentimento, e sim através do material, não é um \\ncaminho digno para seguir  os conselhos e, muito menos, para \\ncolocá -los ao lado da lider ança.   \\nQuando um líder político miserável aumenta aqueles \\nprodutos básicos de um miserável isso é o início de ser odiado por \\naqueles miseráveis que o amavam, não só por deixar o miserável \\nainda mais na miséria, mas porque esse mesmo movimento gerou \\numa di stribuição exagerada para poucos. Logo, aquela perda para \\naqueles que se sentem prejudicados é a perda para o líder político \\nmiserável, pois aquela necessidade de se viver semelhante aos \\nmiseráveis é a descontinuação e a perda da quantidade de \\nliderados.",
      "position": 72840,
      "chapter": 16,
      "page": 66,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.17627118644067,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 35.4,
        "avg_word_length": 4.9209039548022595,
        "unique_word_ratio": 0.632768361581921,
        "avg_paragraph_length": 177.0,
        "punctuation_density": 0.1016949152542373,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liberdade",
          "aqueles",
          "miserável",
          "através",
          "líder",
          "perda",
          "quando",
          "todos",
          "pois",
          "viver",
          "sentimento",
          "liderados",
          "logo",
          "político",
          "miseráveis",
          "aquela",
          "capítulo",
          "usada",
          "forma",
          "torne"
        ],
        "entities": [
          [
            "16",
            "CARDINAL"
          ],
          [
            "Liberdade",
            "GPE"
          ],
          [
            "quando usada de uma forma",
            "PERSON"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "para aqueles",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "lado da lider ança",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "ainda mais na miséria",
            "PERSON"
          ],
          [
            "exagerada",
            "GPE"
          ]
        ],
        "readability_score": 80.82372881355933,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 112,
        "lexical_diversity": 0.632768361581921
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "Um grande líder político tem que ter outros líderes \\nsecundários com um pensamento de liderança semelhante ao \\nmaior líder. Os mesmos líderes secundários que o seguem não \\npodem ter uma liberdade financeira e muito menos vícios, pois os \\nmiseráveis que vivem na miséria não querem um líder que não \\nseja exemplo. Logo, aqueles miseráveis enxergam o líder como \\nsemelhante, um líder que gasta pouco é bem -visto por aqueles que \\no seguem, não pela semelhança da miséria, e sim por seu custo de \\nvida não ser de causar i nveja. Assim, o miserável se sente seguro \\nem não ser roubado, e esse líder não se importa com a fama de ser \\nmiserável, porque esse rótulo é um  \\ndaqueles “defeitos” que o faz ser admirado.   \\n“Um líder político miserável , quando fizer algo errado, deve  \\nutilizar esse erro para beneficiar a  \\ntodos e não a si próprio.”   \\nAssim como o maior líder, em uma hierarquia, não pode \\nexaltar o luxo, os líderes secundários também não podem usufruir \\ndo luxo da vida, pois além de serem exemplos para uma \\nquantidade de miserá veis, também são para outros líderes \\nsecundários e para outras frentes miseráveis. Assim, aqueles",
      "position": 74068,
      "chapter": 3,
      "page": 67,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.35434462444772,
      "complexity_metrics": {
        "word_count": 194,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.714285714285715,
        "avg_word_length": 4.752577319587629,
        "unique_word_ratio": 0.6082474226804123,
        "avg_paragraph_length": 194.0,
        "punctuation_density": 0.1134020618556701,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "líderes",
          "secundários",
          "miseráveis",
          "aqueles",
          "assim",
          "miserável",
          "esse",
          "político",
          "outros",
          "semelhante",
          "maior",
          "seguem",
          "podem",
          "pois",
          "miséria",
          "como",
          "vida",
          "luxo",
          "também"
        ],
        "entities": [
          [
            "financeira e muito",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "semelhança da miséria",
            "PERSON"
          ],
          [
            "importa",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "quando fizer",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "também não podem",
            "PERSON"
          ],
          [
            "também são",
            "PERSON"
          ],
          [
            "para outros",
            "PERSON"
          ]
        ],
        "readability_score": 84.71708394698085,
        "semantic_density": 0,
        "word_count": 194,
        "unique_words": 118,
        "lexical_diversity": 0.6082474226804123
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "líderes secundários não podem se sentir inferiores, pois a \\ninferioridade é a causa da ganância para aqueles que se sentem \\ninferiores. Logo, percebemos que a l iberdade que um líder pode \\nter deve ser  proporcional à liberdade de todos que estão no \\nalicerce da liderança.",
      "position": 75325,
      "chapter": 3,
      "page": 68,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.743333333333332,
      "complexity_metrics": {
        "word_count": 45,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 22.5,
        "avg_word_length": 4.977777777777778,
        "unique_word_ratio": 0.8444444444444444,
        "avg_paragraph_length": 45.0,
        "punctuation_density": 0.08888888888888889,
        "line_break_count": 4,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "inferiores",
          "líderes",
          "secundários",
          "podem",
          "sentir",
          "pois",
          "inferioridade",
          "causa",
          "ganância",
          "aqueles",
          "sentem",
          "logo",
          "percebemos",
          "iberdade",
          "líder",
          "pode",
          "deve",
          "proporcional",
          "liberdade",
          "todos"
        ],
        "entities": [
          [
            "da ganância para aqueles",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ]
        ],
        "readability_score": 87.25666666666666,
        "semantic_density": 0,
        "word_count": 45,
        "unique_words": 38,
        "lexical_diversity": 0.8444444444444444
      },
      "preservation_score": 6.023026697645126e-07
    },
    {
      "id": 1,
      "text": "Capítulo 17   \\nCaos e felicidade; é melhor ser feliz no caos, ou antes em caos \\nque ser feliz   \\nAntes mesmo de começar a falar sobre este capítulo, \\ntemos que lembrar que nós miseráveis somos tão falhos que as \\nnossas imbecilidades são sempre as mesmas, assim todos os \\nassun tos abordados neste livro são ciclos repetitivos de erros \\nproporcionais a um viver miserável... Logo, por muitas vezes, a \\nescrita e a leitura se tornam maçantes, não pela falta de \\nargumentos na escrita, e sim pela própria imbecilidade dos \\nmiseráveis, pois  independentemente de qual seja o miserável, é \\npossível observar que só muda a dimensão do erro e não o erro, \\nporém é necessário que a dimensão dos erros seja escrita e falada, \\naté porque se alguém chegou a essa escala social foi obrigado a \\nviver e passar por outras imbecilidades. Formas de se perder na \\nvida devido ao próprio pensar melhor:   \\nImaginar que uma vida a qual você está olhando é melhor que a \\nsua.   \\nTer inveja de algo, sem saber que aquele algo pode ser ruim, \\nquando se tem.",
      "position": 75924,
      "chapter": 17,
      "page": 70,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.38938547486033,
      "complexity_metrics": {
        "word_count": 179,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 44.75,
        "avg_word_length": 4.631284916201118,
        "unique_word_ratio": 0.7094972067039106,
        "avg_paragraph_length": 179.0,
        "punctuation_density": 0.11731843575418995,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "melhor",
          "escrita",
          "capítulo",
          "feliz",
          "antes",
          "miseráveis",
          "imbecilidades",
          "erros",
          "viver",
          "miserável",
          "pela",
          "qual",
          "seja",
          "dimensão",
          "erro",
          "vida",
          "algo",
          "felicidade",
          "mesmo"
        ],
        "entities": [
          [
            "17",
            "CARDINAL"
          ],
          [
            "miseráveis",
            "PRODUCT"
          ],
          [
            "mesmas",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "ciclos repetitivos de erros",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Formas de se",
            "PERSON"
          ],
          [
            "Imaginar",
            "PERSON"
          ]
        ],
        "readability_score": 76.23561452513967,
        "semantic_density": 0,
        "word_count": 179,
        "unique_words": 127,
        "lexical_diversity": 0.7094972067039106
      },
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "id": 1,
      "text": "Não pensar que pensa r algo ruim seja ruim.   \\nDeixar o nosso sentimento ser contra o viver do outro.   \\nO nosso viver não é melhor por aqueles que temos respeito e \\nconfiança.   \\nNosso viver não tem e nem precisa ser melhor ou pior que o de \\nalguém.   \\nTer medo do seu próprio senti mento e do seu próprio viver.   \\nPensar que o nosso estudo é melhor e definitivo.   \\nNão analisarmos e interpretarmos a nós mesmos.   \\nPensar que sempre a melhor resposta é se omitir. Pensar que nós \\nnão somos capazes de fazer algo.   \\nTer vergonha de si própri o.   \\nAgora que já mencionamos a necessidade de repetir as \\nmesmas imbecilidades dos miseráveis, vamos observar outras \\nquestões, pois um político miserável deve ter cuidado para saber \\nquais são os sujeitos que estão ao seu lado. Caso ele não saiba \\nusar a sab edoria, logo será agressivo. No entanto, cabe pontuar \\nque esse político miserável agressivo não é de todo mal, até",
      "position": 77116,
      "chapter": 3,
      "page": 71,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.520721153846154,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 12.307692307692308,
        "avg_word_length": 4.55625,
        "unique_word_ratio": 0.69375,
        "avg_paragraph_length": 160.0,
        "punctuation_density": 0.10625,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pensar",
          "nosso",
          "viver",
          "melhor",
          "algo",
          "ruim",
          "próprio",
          "político",
          "miserável",
          "agressivo",
          "pensa",
          "seja",
          "deixar",
          "sentimento",
          "contra",
          "outro",
          "aqueles",
          "temos",
          "respeito",
          "confiança"
        ],
        "entities": [
          [
            "Deixar",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "Nosso",
            "PERSON"
          ],
          [
            "nem precisa ser melhor",
            "PERSON"
          ],
          [
            "Pensar",
            "PERSON"
          ],
          [
            "Não",
            "PERSON"
          ],
          [
            "Pensar",
            "PERSON"
          ],
          [
            "já mencionamos",
            "PERSON"
          ],
          [
            "para saber \\n",
            "PERSON"
          ]
        ],
        "readability_score": 92.47927884615385,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 111,
        "lexical_diversity": 0.69375
      },
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "id": 1,
      "text": "porque temos situações em que a agressividade é necessária não \\npor ser agressivo, e sim por limitar aqueles que estão errados \\ndiante do conte xto dos miseráveis. Como mencionado \\nanteriormente aqui, a dificuldade territorial nos faz ser \\nbenevolentes à crueldade pela necessidade de viver melhor.   \\nUm político miserável agressivo não pode temer a sua \\nagressividade, pois temer perante a sua própria conquista, desde \\nque por ela mantenha os miseráveis unidos, não por ser piedoso \\npela necessidade de querer o exagero caótico para controlar o \\npróprio caos, pois nós miserávamos , quando não concordamos, o \\ncaos se torna a necessidade para adaptar -se, até porq ue só dessa \\nforma para tentar compreender e entender o saber do ódio alheio. \\nSe o político miserável agressivo conquista os miseráveis pela \\nagressividade, saber o seu limite de quanto ruim o outro pode ser \\né necessário para a sua própria evolução.   \\n“Antes  de qualquer coisa, temos que nos questionar: o que \\né humanidade? Não somos um padrão de humanos, logo a \\nresposta para a pergunta é que a de humanidade significa  \\no sentimento em comum da maioria.”",
      "position": 78155,
      "chapter": 3,
      "page": 72,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.596153846153847,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 5.082417582417582,
        "unique_word_ratio": 0.6483516483516484,
        "avg_paragraph_length": 182.0,
        "punctuation_density": 0.1043956043956044,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "agressividade",
          "agressivo",
          "miseráveis",
          "pela",
          "necessidade",
          "temos",
          "político",
          "miserável",
          "pode",
          "temer",
          "pois",
          "própria",
          "conquista",
          "caos",
          "saber",
          "humanidade",
          "porque",
          "situações",
          "necessária",
          "limitar"
        ],
        "entities": [
          [
            "porque temos situações",
            "PERSON"
          ],
          [
            "conte xto",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "exagero caótico para controlar",
            "PERSON"
          ],
          [
            "nós miserávamos",
            "ORG"
          ],
          [
            "quando não concordamos",
            "PERSON"
          ],
          [
            "para tentar compreender",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "seu limite de quanto",
            "ORG"
          ]
        ],
        "readability_score": 85.47527472527473,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 118,
        "lexical_diversity": 0.6483516483516484
      },
      "preservation_score": 1.490699107667169e-05
    },
    {
      "id": 1,
      "text": "As duras condições da vida, devido ao trajeto agressivo, \\nfazem os sujeitos se questionarem sobre a possibilidade de o \\npolítico miserável agressivo se respaldar das situações agressivas \\nadversas. Essas situações trazem uma questão: é melhor ser \\nconfiável ag ressivo ou o contrário? Pensando na ausência da \\nconfiança, é melhor ir para o lado da ganância, pois essa é a maior \\ncausadora da fome, logo tem -se o ditado “aquele que tem fome \\ntem pressa”.   \\nO trajeto desse político miserável agressivo junto aos \\nmiserávei s que adquiriu pela ganância e não pela confiança e pelo \\nsentimento deve ser observado, pois nós somos ruins pelo medo \\nde sermos inferiores a outros miseráveis, o que gera uma eterna \\nnecessidade de ser superior aos outros miseráveis. Por serem \\nmiseráveis a gressivos, não conseguem enxergar as oportunidades \\nna confiança, pois não enxergam como benefício e isso ocorre \\ndevido ao próprio viver em caos.   \\nUm político miserável agressivo pode muito bem coexistir \\nem ser confiável, agressivo e ganancioso, pois essas  são as \\ncaracterísticas que o fizeram ser um líder político. No entanto, \\npara isso acontecer e dar certo são necessários sacrifícios",
      "position": 79403,
      "chapter": 3,
      "page": 73,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.79050193050193,
      "complexity_metrics": {
        "word_count": 185,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 26.428571428571427,
        "avg_word_length": 5.254054054054054,
        "unique_word_ratio": 0.6864864864864865,
        "avg_paragraph_length": 185.0,
        "punctuation_density": 0.10270270270270271,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "agressivo",
          "político",
          "pois",
          "miserável",
          "confiança",
          "miseráveis",
          "devido",
          "trajeto",
          "situações",
          "essas",
          "melhor",
          "confiável",
          "ganância",
          "fome",
          "pela",
          "pelo",
          "outros",
          "isso",
          "duras",
          "condições"
        ],
        "entities": [
          [
            "questionarem",
            "PERSON"
          ],
          [
            "ausência da \\nconfiança",
            "PERSON"
          ],
          [
            "lado da ganância",
            "PERSON"
          ],
          [
            "aos \\nmiserávei s que",
            "ORG"
          ],
          [
            "ganância e não pela confiança e pelo \\nsentimento deve",
            "PERSON"
          ],
          [
            "nós somos",
            "ORG"
          ],
          [
            "pelo medo \\nde sermos",
            "PERSON"
          ],
          [
            "aos outros miseráveis",
            "ORG"
          ],
          [
            "muito bem coexistir \\nem",
            "PERSON"
          ],
          [
            "características que",
            "ORG"
          ]
        ],
        "readability_score": 85.20949806949807,
        "semantic_density": 0,
        "word_count": 185,
        "unique_words": 127,
        "lexical_diversity": 0.6864864864864865
      },
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "id": 1,
      "text": "prazerosos, pois viver agressivamente requer sabedoria em se \\nmovimentar, já que todos os outros miseráveis vão observar, um a \\nvez que não concordam, mas são de comum acordo com a \\nagressividade do líder, pois são muitos sentimentais para aguentar \\na agressividade. Agora, vejamos alguns desses sacrifícios \\nprazerosos:    \\nSexo – os velhos miseráveis, ao falar de sexo, pensam que o \\nhomem é o único que pode fazer sexo. Na religião, o ato de fazer \\nsexo antes do casamento é muito agressivo para a doutrina \\nreligiosa. Creio eu que esses são os que mais vão ter preconceitos \\nneste tópico, pois aqueles que pensam assim são os mesmos que \\ncriam  filhos miseráveis.   \\nDroga – aqui neste tópico só a palavra vem com peso, o peso o \\nqual eu não entendo, pois os miseráveis que julgam não entendem \\no significado da palavra droga, pois tem peso para o lado ruim da \\npalavra só quando convém a quem usa. No en tanto, muitas vezes \\nesses sujeitos são drogados em remédios, açúcar, sódio, comida, \\nmusculação, incômodo, certeza, estudo e tudo aquilo que pode ser \\nchamado de vício.",
      "position": 80699,
      "chapter": 3,
      "page": 74,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.531952117863725,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.166666666666668,
        "avg_word_length": 4.828729281767956,
        "unique_word_ratio": 0.6850828729281768,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.15469613259668508,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "miseráveis",
          "sexo",
          "palavra",
          "peso",
          "prazerosos",
          "agressividade",
          "pensam",
          "pode",
          "fazer",
          "esses",
          "neste",
          "tópico",
          "droga",
          "viver",
          "agressivamente",
          "requer",
          "sabedoria",
          "movimentar",
          "todos"
        ],
        "entities": [
          [
            "outros miseráveis",
            "GPE"
          ],
          [
            "mas são de comum acordo",
            "PERSON"
          ],
          [
            "para aguentar",
            "PERSON"
          ],
          [
            "Agora",
            "PERSON"
          ],
          [
            "único",
            "GPE"
          ],
          [
            "ato de fazer",
            "ORG"
          ],
          [
            "casamento é muito agressivo para",
            "ORG"
          ],
          [
            "Creio eu",
            "PERSON"
          ],
          [
            "mesmos que",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ]
        ],
        "readability_score": 83.46804788213628,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 124,
        "lexical_diversity": 0.6850828729281768
      },
      "preservation_score": 1.897253409758215e-05
    },
    {
      "id": 1,
      "text": "Felicidade – aqui neste tópico é necessário pontuar que até a \\nforma de se vestir fora de um padrão é julgada como errada. Ter \\numa casa, um carro, fazer uma viagem e tudo aquilo que possa \\ndemonstrar felicidade não são ações dignas para um político \\nagressivo miserável viver, lembrando que os miseráveis \\nagressivos esquecem mais rapidamente a m orte de um pai do que \\na perda de uma ganância conquistada.   \\nEm alguns trajetos, o valor monetário gerado por um bem \\nfamiliar está associado a viver no melhor conforto e é o legado \\nsentimental deixado por uma estrutura familiar. Logo, \\npercebemos que a agre ssividade, quando equilibrada, serve para \\nenxergar que também é necessário ser agressivo para ser um \\ngrande líder familiar e territorial. O sentimento que gerou uma \\nconquista digna, quando permanecer no caráter do humano, não \\nimplicará o entendimento de er rar e me desculpar, pois a \\nconquista através do próprio caráter significa o valor e o tamanho \\nda conquista.",
      "position": 81896,
      "chapter": 3,
      "page": 75,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.5944099378882,
      "complexity_metrics": {
        "word_count": 161,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 32.2,
        "avg_word_length": 4.9813664596273295,
        "unique_word_ratio": 0.6894409937888198,
        "avg_paragraph_length": 161.0,
        "punctuation_density": 0.09316770186335403,
        "line_break_count": 16,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "familiar",
          "conquista",
          "felicidade",
          "necessário",
          "agressivo",
          "viver",
          "valor",
          "quando",
          "caráter",
          "aqui",
          "neste",
          "tópico",
          "pontuar",
          "forma",
          "vestir",
          "fora",
          "padrão",
          "julgada",
          "como",
          "errada"
        ],
        "entities": [
          [
            "necessário",
            "GPE"
          ],
          [
            "forma de se",
            "PERSON"
          ],
          [
            "vestir fora de um padrão",
            "PERSON"
          ],
          [
            "julgada como errada",
            "ORG"
          ],
          [
            "uma viagem",
            "ORG"
          ],
          [
            "tudo aquilo",
            "PERSON"
          ],
          [
            "que possa \\ndemonstrar",
            "PERSON"
          ],
          [
            "ações dignas",
            "PERSON"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "monetário gerado",
            "PERSON"
          ]
        ],
        "readability_score": 82.4055900621118,
        "semantic_density": 0,
        "word_count": 161,
        "unique_words": 111,
        "lexical_diversity": 0.6894409937888198
      },
      "preservation_score": 9.034540046467691e-06
    },
    {
      "id": 1,
      "text": "Capítulo 18   \\nDe que modo os líderes não perdem a confiança   \\n   “A lealdade dos miseráveis baseia -se na quantidade de \\nmiseráveis coexist entes no mesmo caráter. Quando esse caráter \\nnão sabe  \\nser usado, são julgados como animais.”   \\nUm político miserável, quando chega a uma liderança, \\npara se manter, basta ser digno com as palavras ditas ao decorrer \\ndo trajeto, pois aqueles que não são dignos com as suas próprias \\npalavras terão como consequência a crítica de muitos.  Isso será \\nalarman te para a sua liderança.   \\nDeve saber, então, que existem duas formas de “tampar \\nburacos”: uma com regras, a outra com o uso da força. A primeira \\nestá associada aos próprios erros dos miseráveis, a segunda, por \\nsua vez, está atrelada ao instinto primitivo dos miseráveis. Porém, \\ncomo a primeira contém falhas, ocorre a necessidade de recorrer \\nà segunda. “Nossos instintos primitivos são os instintos que nos \\ncausam histeria e, quando eles não são controlados, causam a \\nausência do sentimento humano.”",
      "position": 83006,
      "chapter": 18,
      "page": 76,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.579779158040026,
      "complexity_metrics": {
        "word_count": 161,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 17.88888888888889,
        "avg_word_length": 5.080745341614906,
        "unique_word_ratio": 0.7391304347826086,
        "avg_paragraph_length": 161.0,
        "punctuation_density": 0.14906832298136646,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "quando",
          "como",
          "caráter",
          "liderança",
          "palavras",
          "primeira",
          "está",
          "segunda",
          "instintos",
          "causam",
          "capítulo",
          "modo",
          "líderes",
          "perdem",
          "confiança",
          "lealdade",
          "baseia",
          "quantidade",
          "coexist"
        ],
        "entities": [
          [
            "18",
            "CARDINAL"
          ],
          [
            "não perdem",
            "PERSON"
          ],
          [
            "baseia -se",
            "PERSON"
          ],
          [
            "na quantidade de \\nmiseráveis",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "para se manter",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "Deve",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ]
        ],
        "readability_score": 89.53133195307109,
        "semantic_density": 0,
        "word_count": 161,
        "unique_words": 119,
        "lexical_diversity": 0.7391304347826086
      },
      "preservation_score": 2.1005305608037384e-05
    },
    {
      "id": 1,
      "text": "Sendo ass im, é necessário que um político miserável saiba \\ndoutrinar os seus instintos, pois aqueles que agem pelo impulso \\nnão conhecem os seus erros, já que eles formam o caráter, seja no \\naspecto benéfico, seja no aspecto “maquiavélico”. Os aspectos \\nnegativos nos c ausam incoerência a um bem em comum e nos \\ncausam uma coerência a um benefício em comum. Imagina se \\ntodos os miseráveis fossem humanos bons, logo, não existiria os \\nmiseráveis maus. Assim, é necessário observar que o mesmo \\ncaráter tem peso relativo.  Veja al guns questionamentos:    \\nQual é o valor do caráter de um guerreiro na favela para esse \\nterritório?   \\nQual é o valor do caráter de um guerreiro trabalhador para o \\nterritório?   \\nExemplo: Aquele miserável bonzinho, muito bonzinho mesmo, \\nacima da média, quando  é bom demais, outros miseráveis vão \\nusufruir excessivamente de sua bondade.   \\n“Todos nós temos um caráter dominante, ele  serve para beneficiar \\nou prejudicar, só depende  \\nde como é direcionado.”",
      "position": 84168,
      "chapter": 3,
      "page": 77,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.31981599433829,
      "complexity_metrics": {
        "word_count": 157,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 17.444444444444443,
        "avg_word_length": 5.140127388535032,
        "unique_word_ratio": 0.7133757961783439,
        "avg_paragraph_length": 157.0,
        "punctuation_density": 0.15286624203821655,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caráter",
          "miseráveis",
          "necessário",
          "miserável",
          "seus",
          "seja",
          "aspecto",
          "comum",
          "todos",
          "mesmo",
          "qual",
          "valor",
          "guerreiro",
          "território",
          "bonzinho",
          "sendo",
          "político",
          "saiba",
          "doutrinar",
          "instintos"
        ],
        "entities": [
          [
            "Sendo",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "Imagina se \\n",
            "PERSON"
          ],
          [
            "miseráveis",
            "PRODUCT"
          ],
          [
            "fossem humanos bons",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Veja al",
            "PERSON"
          ],
          [
            "muito bonzinho mesmo",
            "PERSON"
          ],
          [
            "acima da média",
            "PERSON"
          ]
        ],
        "readability_score": 89.73573956121727,
        "semantic_density": 0,
        "word_count": 157,
        "unique_words": 112,
        "lexical_diversity": 0.7133757961783439
      },
      "preservation_score": 1.897253409758215e-05
    },
    {
      "id": 1,
      "text": "A dificuldade de um político miserável está em todas as \\nfrentes, começa com o pensamento primitivo de julgar um padrão \\nvisual de outro estilo de vida perante uma vida que não \\nprecisamos julgar. Assim, o político miserável não possui todas \\nas qualidades, um a vez que só é necessário aparentar ter. No \\nentanto, isso não está atrelado a ganhar poder, pois o poder pode \\nser adquirido de muitas formas, uma dessas formas é a quantidade \\nde negócios que um político miserável consegue fazer na surdina, \\npois esses negóc ios, na maioria das vezes, beneficiam uma em mil \\npessoas. No entanto, são esses sujeitos que fazem aliança com \\noutros políticos miseráveis, é importante lembrar que os líderes \\nnão podem praticar todas aquelas ações dos miseráveis que são \\nconsiderados bons.  Logo, chegamos a uma conclusão: os \\nmiseráveis apreciam uma aparência melhor devido aos nossos \\nolhos enxergarem aquilo que querem que enxerguemos.   \\n “E os miseráveis , em geral , julgam mais pelos olhos do que pela \\nconfiança, porque a todos cabe ver.”    \\n  Precisamos entender  que a  mesma quantidade de \\nmiseráveis que você comanda é a mesma que te cobra. Portanto,",
      "position": 85280,
      "chapter": 3,
      "page": 78,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.259625668449196,
      "complexity_metrics": {
        "word_count": 187,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.375,
        "avg_word_length": 5.032085561497326,
        "unique_word_ratio": 0.6524064171122995,
        "avg_paragraph_length": 187.0,
        "punctuation_density": 0.12834224598930483,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "político",
          "miserável",
          "todas",
          "está",
          "julgar",
          "vida",
          "precisamos",
          "entanto",
          "poder",
          "pois",
          "formas",
          "quantidade",
          "esses",
          "olhos",
          "mesma",
          "dificuldade",
          "frentes",
          "começa",
          "pensamento"
        ],
        "entities": [
          [
            "precisamos julgar",
            "PERSON"
          ],
          [
            "político miserável não possui",
            "FAC"
          ],
          [
            "ser adquirido de muitas",
            "ORG"
          ],
          [
            "beneficiam uma",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "apreciam uma aparência melhor devido aos nossos",
            "PERSON"
          ],
          [
            "que querem que enxerguemos",
            "PERSON"
          ],
          [
            "julgam mais pelos",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Precisamos",
            "ORG"
          ]
        ],
        "readability_score": 86.8028743315508,
        "semantic_density": 0,
        "word_count": 187,
        "unique_words": 122,
        "lexical_diversity": 0.6524064171122995
      },
      "preservation_score": 1.7617353090611997e-05
    },
    {
      "id": 1,
      "text": "a miséria se torna necessária para se ter mão de obra para \\nalimentar melhor aqueles que vivem de aparência.   \\nPercebemos que um político miser ável pode aparentar ser \\nde muitas formas, porém poucos vão entender e sentir aquilo que \\nvocê é. Assim, os meios necessários, seja pela ganância, seja pela \\nconfiança, sempre vão ser julgados honrosos e por todos \\nlouvados, porque os miseráveis sempre se deix am levar pelas \\naparências e pelos resultados.    \\n“Os poucos políticos miseráveis não podem existir quando os \\nmuitos miseráveis têm como  se apoiar...”   \\nOs próximos são mais semelhantes ao seu caráter, assim, \\ntornam -se transmissores de caráter. Quanto mais  visível você for, \\nmais pessoas em seu entorno é necessário ter para melhorar a \\ncompreensão do seu caráter.  Quanto maior a liderança através do \\ncaráter, menores serão as chances de um político miserável obter \\na aceitação de todos. Desse modo, isso o torna  cego para aqueles \\npolíticos miseráveis e os demais miseráveis que estão próximos \\npelo interesse na própria liderança.",
      "position": 86552,
      "chapter": 3,
      "page": 79,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.883841463414633,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 20.5,
        "avg_word_length": 5.237804878048781,
        "unique_word_ratio": 0.7012195121951219,
        "avg_paragraph_length": 164.0,
        "punctuation_density": 0.12804878048780488,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "caráter",
          "mais",
          "torna",
          "aqueles",
          "político",
          "poucos",
          "você",
          "assim",
          "seja",
          "pela",
          "sempre",
          "todos",
          "políticos",
          "próximos",
          "quanto",
          "liderança",
          "miséria",
          "necessária",
          "obra"
        ],
        "entities": [
          [
            "para se ter",
            "PERSON"
          ],
          [
            "alimentar melhor",
            "ORG"
          ],
          [
            "de aparência",
            "PERSON"
          ],
          [
            "Percebemos",
            "PERSON"
          ],
          [
            "ser \\nde muitas",
            "ORG"
          ],
          [
            "confiança",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "deix am levar",
            "ORG"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ]
        ],
        "readability_score": 88.17865853658536,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 115,
        "lexical_diversity": 0.7012195121951219
      },
      "preservation_score": 1.5358718078995074e-05
    },
    {
      "id": 1,
      "text": "Capítulo 19   \\nComo evitar “o lado negro da força”   \\nComo já falei sobre muitas qualidades importantes, \\ntentarei ser mais objetivo, ressaltando estas qualidades: evitar \\naquelas circunstâncias que possam ser incômodas e cumprir com \\nas palavras ditas. Logo, não haverá situação que possa se \\ntransformar em caos.    \\nNem todos os miseráveis conseguem ter uma profissão \\nque possa dar um luxo para viver uma vida com felicidades, pois \\nusufruir da felicidade é a causa da inveja para os miseráveis \\ninvejosos, por isso é importante selecionar miseráveis de \\nconfiança para es tar próximo, assim há menos chances de ser \\nprejudicado. A facilidade em prejudicar através do instinto \\nsexual, que é o maior impulso da ganância, serve para se ter uma \\nfamília e um estilo de vida.   \\nO político miserável deve manter -se em um equilíbrio \\npara que ninguém possa querer enganar ou trair. Para conseguir \\nessa façanha, precisa ter um",
      "position": 87724,
      "chapter": 19,
      "page": 80,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.79081632653061,
      "complexity_metrics": {
        "word_count": 147,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 24.5,
        "avg_word_length": 5.136054421768708,
        "unique_word_ratio": 0.7551020408163265,
        "avg_paragraph_length": 147.0,
        "punctuation_density": 0.10204081632653061,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "possa",
          "miseráveis",
          "como",
          "evitar",
          "qualidades",
          "vida",
          "capítulo",
          "lado",
          "negro",
          "força",
          "falei",
          "muitas",
          "importantes",
          "tentarei",
          "mais",
          "objetivo",
          "ressaltando",
          "estas",
          "aquelas",
          "circunstâncias"
        ],
        "entities": [
          [
            "19",
            "CARDINAL"
          ],
          [
            "lado negro da força",
            "PERSON"
          ],
          [
            "Nem",
            "PERSON"
          ],
          [
            "tar próximo",
            "PERSON"
          ],
          [
            "essa façanha",
            "ORG"
          ]
        ],
        "readability_score": 86.20918367346938,
        "semantic_density": 0,
        "word_count": 147,
        "unique_words": 111,
        "lexical_diversity": 0.7551020408163265
      },
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "id": 1,
      "text": "“network” de confiança. Essa “solução” é a prevenção do próprio \\nerro para manter -se em uma posição estabilizada, para isso tem \\nque estar rodeado de pessoas de confian ça, os mesmos que fazem \\num pequeno círculo de confiança são aqueles que criam as \\nbarreiras contra a desconfiança, pois são aqueles que te dão força \\npara ser um melhor líder. Sem eles, o político miserável não \\nconseguiria enxergar a necessidade de evoluir, essa evolução não \\nprecisa ser através do caráter ou pela ganância, ambas podem ser \\nbem-feitas, basta apenas organizar e estabilizar os políticos \\nmiseráveis e os líderes miseráveis do seu entorno.   \\n “Nenhuma economia no mundo cresceu sem roubo.”   \\nO roubo é uma das formas de interpretar a economia, pois \\ntem várias características diferentes.    \\nEm  primeiro  lugar,  precisamos considerar a \\nfalta de agitação da economia, pois geralmente é motivo de \\npreocupação, pois, quando se encontra dessa forma es tá atrelada \\na uma conspiração contra o próprio político miserável.   \\nTemos o excesso de agitação, que vem através da \\nganância, logo, esses gananciosos são fãs do luxo que faz os \\nmiseráveis que vivem na pobreza terem trabalho. Os políticos",
      "position": 88808,
      "chapter": 4,
      "page": 81,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.25040322580645,
      "complexity_metrics": {
        "word_count": 186,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.25,
        "avg_word_length": 5.209677419354839,
        "unique_word_ratio": 0.7096774193548387,
        "avg_paragraph_length": 186.0,
        "punctuation_density": 0.11827956989247312,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "miseráveis",
          "economia",
          "confiança",
          "essa",
          "próprio",
          "aqueles",
          "contra",
          "político",
          "miserável",
          "através",
          "ganância",
          "políticos",
          "roubo",
          "agitação",
          "network",
          "solução",
          "prevenção",
          "erro",
          "manter"
        ],
        "entities": [
          [
            "Essa",
            "PERSON"
          ],
          [
            "de pessoas de confian",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "essa evolução",
            "ORG"
          ],
          [
            "pela ganância",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Nenhuma",
            "PERSON"
          ],
          [
            "Em  primeiro  lugar",
            "ORG"
          ]
        ],
        "readability_score": 86.81209677419355,
        "semantic_density": 0,
        "word_count": 186,
        "unique_words": 132,
        "lexical_diversity": 0.7096774193548387
      },
      "preservation_score": 2.145703261036077e-05
    },
    {
      "id": 1,
      "text": "miseráveis não co nseguem conter a sua própria ganância. No \\nentanto, percebemos que saber balancear o roubo é necessário \\npara uma economia evoluir.   \\nUm político miserável hoje pode estar de bem com os \\nmiseráveis e amanhã pode estar de mal; a perda da confiança de \\num políti co miserável representa a abertura para descobrir o \\nquanto a liderança aproximou os políticos miseráveis errados. \\nQuem sempre conspira não pode estar sozinho, pois começam a \\naparecer grupos conspiratórios para tirar o político miserável do \\npoder, os grupos  prejudicados irão ofender aquele que está \\nprejudicando e, logo, aquele caráter que o fez ser um político \\nmiserável é o mesmo que será mais agredido, não por ser ruim, e \\nsim por ser o motivo para os miseráveis seguirem.   \\nDigo para não se preocupar, pois o s sujeitos que \\nconspiram não são dignos e sábios, logo não sabem manter uma \\nconspiração quando o político não tem nada a temer.   \\nComo conseguir uma maior aceitação quando vários \\nterritórios têm uma forma de controlar o próprio território?   \\nQuando não há o que temer, ainda mais quando o caráter \\né construído através da miséria, o líder conseguirá permanecer na",
      "position": 90110,
      "chapter": 4,
      "page": 82,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.138145100972324,
      "complexity_metrics": {
        "word_count": 191,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.285714285714285,
        "avg_word_length": 4.984293193717278,
        "unique_word_ratio": 0.6282722513089005,
        "avg_paragraph_length": 191.0,
        "punctuation_density": 0.09424083769633508,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "político",
          "miserável",
          "quando",
          "pode",
          "pois",
          "grupos",
          "aquele",
          "logo",
          "caráter",
          "mais",
          "temer",
          "nseguem",
          "conter",
          "própria",
          "ganância",
          "entanto",
          "percebemos",
          "saber",
          "balancear"
        ],
        "entities": [
          [
            "não co nseguem conter a sua própria ganância",
            "ORG"
          ],
          [
            "percebemos que",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "abertura",
            "GPE"
          ],
          [
            "Quem",
            "GPE"
          ],
          [
            "irão",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "seguirem",
            "GPE"
          ],
          [
            "conspiração quando",
            "PERSON"
          ],
          [
            "quando vários",
            "ORG"
          ]
        ],
        "readability_score": 84.86185489902768,
        "semantic_density": 0,
        "word_count": 191,
        "unique_words": 120,
        "lexical_diversity": 0.6282722513089005
      },
      "preservation_score": 1.2874219566216461e-05
    },
    {
      "id": 1,
      "text": "liderança por conhecer o caos da maioria contra os políticos \\nmiseráveis. Viver uma vida antes de assumir o poder foi o que fez \\nter a sabedoria de res ponder e direcionar o caminho a ser seguido, \\nmas nunca deixando de dar importância a outros políticos \\nmiseráveis e líderes miseráveis. Manter o equilíbrio entre os \\nmiseráveis, os líderes miseráveis e os políticos miseráveis é \\nessencial para conseguir a ace itação nos territórios dominados por \\neles.    \\nÉ importante enxergar o caos de outros políticos \\nmiseráveis e líderes miseráveis, como dito antes, que dizem que \\nsem o roubo não tem como a economia evoluir. Logo, vejo que \\nenxergar o caos desses mesmos é neces sário para estabelecer \\nequilíbrio para evoluir, pois eles são aqueles que sempre estão nos \\nlocais em que há mais miseráveis, pelo simples fator de \\nentenderem que o que os fez ser líderes foi estabelecer aliança \\ncom esses grupos. Lá, eles têm o luxo através  da liderança caótica \\ne são aqueles de caráter semelhante a “todos” que vivem em \\nguerra, luxúria, amor, estudo, raça e muitas outras discrepâncias \\nque a miséria proporciona.",
      "position": 91396,
      "chapter": 4,
      "page": 83,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.665018315018315,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.333333333333332,
        "avg_word_length": 4.9945054945054945,
        "unique_word_ratio": 0.6098901098901099,
        "avg_paragraph_length": 182.0,
        "punctuation_density": 0.0989010989010989,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "políticos",
          "líderes",
          "caos",
          "eles",
          "liderança",
          "antes",
          "outros",
          "equilíbrio",
          "enxergar",
          "como",
          "evoluir",
          "estabelecer",
          "aqueles",
          "conhecer",
          "maioria",
          "contra",
          "viver",
          "vida",
          "assumir"
        ],
        "entities": [
          [
            "deixando de dar",
            "PERSON"
          ],
          [
            "Manter",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "como dito",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "vejo que",
            "GPE"
          ],
          [
            "para evoluir",
            "PERSON"
          ],
          [
            "há mais miseráveis",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "luxúria",
            "GPE"
          ]
        ],
        "readability_score": 83.33498168498168,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 111,
        "lexical_diversity": 0.6098901098901099
      },
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "id": 1,
      "text": "Como agradar quem quer viver com liberdade e quem quer viver \\nsem incômodo?   \\nO p olítico miserável não pode ser odiado pelos \\nmiseráveis, pelos líderes miseráveis e os políticos miseráveis, por \\nisso deve então buscar não ser odiado. Para isso, deverá \\nexterminar a fome, pois só assim todas as classes sociais \\nconseguiriam ficar satisfeita s. Entende -se que é impossível que \\nisso ocorra, pois como um trabalhador miserável vai produzir a \\nsua própria casa, comida, roupa, faxina, catar lixo e todas aquelas \\nprofissões que, se a fome acabar, deixariam de existir.    \\nLogo, o que foi citado acima nã o permite construir \\nliberdade e incômodo para todos. Essas duas necessidades de \\nviver têm aspectos bons e ruins, ambas com um peso muito \\ngrande para a vida de quem vive em liberdade na miséria e para \\nquem se sente incomodado no luxo. A maioria dos miseráve is que \\nnecessitam da liberdade não tem outra forma de ser feliz, e aquele \\nque se sente incomodado no luxo não vê felicidade na liberdade, \\npor isso nunca conseguirá admirar a liberdade, já que não viveu \\nem liberdade devido ao medo de que  o próprio luxo o fez t er.",
      "position": 92626,
      "chapter": 4,
      "page": 84,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.276730486008837,
      "complexity_metrics": {
        "word_count": 194,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.714285714285715,
        "avg_word_length": 4.731958762886598,
        "unique_word_ratio": 0.6907216494845361,
        "avg_paragraph_length": 194.0,
        "punctuation_density": 0.11855670103092783,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liberdade",
          "quem",
          "isso",
          "viver",
          "miseráveis",
          "luxo",
          "como",
          "quer",
          "incômodo",
          "miserável",
          "odiado",
          "pelos",
          "fome",
          "pois",
          "todas",
          "sente",
          "incomodado",
          "agradar",
          "olítico",
          "pode"
        ],
        "entities": [
          [
            "Como",
            "ORG"
          ],
          [
            "odiado pelos \\nmiseráveis",
            "PERSON"
          ],
          [
            "pelos",
            "PERSON"
          ],
          [
            "conseguiriam ficar satisfeita s. Entende",
            "PERSON"
          ],
          [
            "casa",
            "GPE"
          ],
          [
            "faxina",
            "GPE"
          ],
          [
            "deixariam de",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Essas",
            "GPE"
          ]
        ],
        "readability_score": 84.72326951399117,
        "semantic_density": 0,
        "word_count": 194,
        "unique_words": 134,
        "lexical_diversity": 0.6907216494845361
      },
      "preservation_score": 1.6262172083641842e-05
    },
    {
      "id": 1,
      "text": "Para conseguir um milagre dessa magnitude, não \\ndevemos juntar um lado com o outro. Assim, não devemos \\njuntar os religiosos com aqueles que não são religiosos, pois \\nessas características são opostas para chegar a um acordo e viver \\nem harmonia.   \\nTemos   também aquele político miserável que vem \\natravés do caso do acaso, esse é aquele que chegou através \\nda “necessidade” para uma mudança radical, não por ser \\nnecessário, e sim pelo desespero de trocar o que a maioria \\npensava que poderia ser melhor. O val or a ser pago pela \\nignorância da necessidade da mudança é a adaptação a um novo \\nlíder o qual nem conhecemos direito, pois o mesmo líder que é \\ncolocado às pressas não tem tempo para adquirir o \\nconhecimento necessário do trajeto. Esse desespero pela \\nmudança raramente funciona, pois o mesmo líder que chegou à \\nliderança sem apoio precisa conquistá -lo durante a sua liderança. \\nAssim, não consegue ter tempo para se dar ao luxo de viver a \\ntrajetória de um miserável, já que o líder precisa ser semelhante \\naos seus li derados. Logo, essa liderança tem grandes chances de \\nter conflitos.",
      "position": 93879,
      "chapter": 4,
      "page": 85,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.732488479262674,
      "complexity_metrics": {
        "word_count": 186,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 26.571428571428573,
        "avg_word_length": 4.82258064516129,
        "unique_word_ratio": 0.6344086021505376,
        "avg_paragraph_length": 186.0,
        "punctuation_density": 0.0967741935483871,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "líder",
          "pois",
          "mudança",
          "liderança",
          "devemos",
          "juntar",
          "assim",
          "religiosos",
          "viver",
          "aquele",
          "miserável",
          "através",
          "esse",
          "chegou",
          "necessidade",
          "necessário",
          "desespero",
          "pela",
          "mesmo",
          "tempo"
        ],
        "entities": [
          [
            "não devemos \\njuntar",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "político miserável que vem",
            "ORG"
          ],
          [
            "para uma mudança radical",
            "PERSON"
          ],
          [
            "pelo desespero de trocar",
            "PERSON"
          ],
          [
            "ignorância da",
            "PERSON"
          ],
          [
            "nem conhecemos direito",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "mesmo",
            "ORG"
          ]
        ],
        "readability_score": 85.26751152073733,
        "semantic_density": 0,
        "word_count": 186,
        "unique_words": 118,
        "lexical_diversity": 0.6344086021505376
      },
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "id": 1,
      "text": "Aquele que quer ser líder precisa ter sabedoria na hora de limitar \\ne ser limitado, ser bom para a maioria ou para a minoria?   \\n“Aquele que se ausenta dos momentos importantes tem \\num julgamento muito difícil a fazer, pois o motivo precisa ser \\nmaior que a ausência.”   \\nPor qual motivo um político miserável chegaria a uma \\nliderança pelo ódio? Pelo mesmo ódio que outros miseráveis \\nodiosos chegariam a esse extremo. Logo, é possível perceber que \\nos semelhantes se atraem por meio da seguinte ideia: minha dor é \\na mesma que a sua. Os sujeitos que praticam numerosos erros \\nagressivos são aqueles miseráveis conquistados pelo medo de \\nserem agred idos ou mortos.    \\nEsse trajeto para a liderança caótica foi alavancado por \\noutros miseráveis caóticos.  \\nChegar ao “trono” é uma consequência de quantos foram \\nbeneficiados pelo caos, essa dificuldade em viver de forma \\ncaótica “mente” para satisfazer as lux úrias da ganância que estão \\natreladas ao aspecto monetário. Logo, uma liderança através do \\ncaos está acompanhada de um “holofote monetário”, pois os \\npolíticos miseráveis agressivos, através dos beneficiados,",
      "position": 95102,
      "chapter": 4,
      "page": 86,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.4032196969697,
      "complexity_metrics": {
        "word_count": 176,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 19.555555555555557,
        "avg_word_length": 5.232954545454546,
        "unique_word_ratio": 0.7045454545454546,
        "avg_paragraph_length": 176.0,
        "punctuation_density": 0.09659090909090909,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pelo",
          "miseráveis",
          "liderança",
          "aquele",
          "precisa",
          "pois",
          "motivo",
          "ódio",
          "outros",
          "esse",
          "logo",
          "agressivos",
          "caótica",
          "beneficiados",
          "caos",
          "monetário",
          "através",
          "quer",
          "líder",
          "sabedoria"
        ],
        "entities": [
          [
            "na hora de limitar \\ne",
            "PERSON"
          ],
          [
            "julgamento muito difícil",
            "ORG"
          ],
          [
            "ausência",
            "GPE"
          ],
          [
            "Pelo",
            "PERSON"
          ],
          [
            "chegariam",
            "PERSON"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "agressivos são aqueles miseráveis",
            "WORK_OF_ART"
          ],
          [
            "pelo medo de \\nserem",
            "PERSON"
          ],
          [
            "outros miseráveis",
            "PERSON"
          ],
          [
            "caóticos",
            "PERSON"
          ]
        ],
        "readability_score": 88.65233585858586,
        "semantic_density": 0,
        "word_count": 176,
        "unique_words": 124,
        "lexical_diversity": 0.7045454545454546
      },
      "preservation_score": 1.788086050863397e-05
    },
    {
      "id": 1,
      "text": "precisam ter muita confiança, já que eles podem fazer evoluir, \\n“desvoluir ou involuir”.    \\n“Os mesmos que chegaram à  liderança  através do ódio, esse \\nmesmo ódio, em escala de tamanho de importância na política, é \\na  \\nproporção do ódio no entorno da liderança.”   \\nO político e o líder miserável agressivo qu e assumiram a \\nliderança através de um caso do acaso, que não ocorreu de forma \\n“digna” e em um padrão, enfrentam a consequência da herança, \\ndo ódio, do roubo, dos erros, dos excessos, da ganância, e outras \\nquestões que estão fora de um padrão territorial de  aceitação. Essa \\nforma de politicagem não é vista de uma forma boa, pois é a \\ngrande causadora da morte do político e do líder miserável \\nodioso.",
      "position": 96341,
      "chapter": 4,
      "page": 87,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.793852459016392,
      "complexity_metrics": {
        "word_count": 122,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 30.5,
        "avg_word_length": 4.729508196721311,
        "unique_word_ratio": 0.6557377049180327,
        "avg_paragraph_length": 122.0,
        "punctuation_density": 0.14754098360655737,
        "line_break_count": 13,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ódio",
          "liderança",
          "forma",
          "através",
          "político",
          "líder",
          "miserável",
          "padrão",
          "precisam",
          "muita",
          "confiança",
          "eles",
          "podem",
          "fazer",
          "evoluir",
          "desvoluir",
          "involuir",
          "mesmos",
          "chegaram",
          "esse"
        ],
        "entities": [
          [
            "precisam",
            "GPE"
          ],
          [
            "consequência da herança",
            "PERSON"
          ],
          [
            "da ganância",
            "PERSON"
          ],
          [
            "fora de um padrão",
            "ORG"
          ],
          [
            "Essa \\nforma de",
            "PERSON"
          ],
          [
            "vista de uma forma boa",
            "ORG"
          ]
        ],
        "readability_score": 83.33114754098361,
        "semantic_density": 0,
        "word_count": 122,
        "unique_words": 80,
        "lexical_diversity": 0.6557377049180327
      },
      "preservation_score": 1.1744902060407997e-05
    },
    {
      "id": 1,
      "text": "Capítulo 20   \\nO excesso de dinheiro, o materialismo e outras questões feitas \\npelo político miserável são úteis ou não?   \\nComo já foi mencionado, muitas vezes há a necessidade \\nde ser benevolente a um crime ou até mesmo, por muitas vezes, é \\nnecessário participar. Nesse co ntexto, outros miseráveis odiosos \\naproveitam -se das necessidades do político miserável odioso para \\nse beneficiar de bens materiais, uns se beneficiam tanto que \\narruínam a vida.    \\n Lembrando que três aspectos são necessários para viver \\nbem: saber movimentar -se entre o meu viver miserável \\nnecessário, o necessário para o meu entorno miserável e o \\nnecessário para os miseráveis.    \\n“Esses indivíduos são cheios de formas diferentes de \\ninterpretar, diferentes formas de sofrer o próprio caos.”   \\nAdemais, cabe ressaltar que jamais existiu um político \\nnovo que tirasse a ganância daqueles políticos miseráveis e, \\naqueles outros bons políticos miseráveis que tinham pouca \\nganância necessitavam ter um pouco mais de ganância, já que não \\nconseguiam praticar alguns atos, uma vez que os seus trajetos não \\nos conduziam a certos tipos de pensamentos.",
      "position": 97199,
      "chapter": 20,
      "page": 88,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.03875968992248,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 28.666666666666668,
        "avg_word_length": 5.406976744186046,
        "unique_word_ratio": 0.686046511627907,
        "avg_paragraph_length": 172.0,
        "punctuation_density": 0.11046511627906977,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miserável",
          "necessário",
          "miseráveis",
          "político",
          "ganância",
          "muitas",
          "vezes",
          "outros",
          "viver",
          "formas",
          "diferentes",
          "políticos",
          "capítulo",
          "excesso",
          "dinheiro",
          "materialismo",
          "outras",
          "questões",
          "feitas",
          "pelo"
        ],
        "entities": [
          [
            "20",
            "CARDINAL"
          ],
          [
            "pelo político",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "ntexto",
            "ORG"
          ],
          [
            "outros miseráveis",
            "GPE"
          ],
          [
            "se beneficiam",
            "PERSON"
          ],
          [
            "Lembrando",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "meu entorno",
            "PRODUCT"
          ]
        ],
        "readability_score": 84.04457364341086,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 118,
        "lexical_diversity": 0.686046511627907
      },
      "preservation_score": 1.7316201755729746e-05
    },
    {
      "id": 1,
      "text": "Essas adversidades dos políticos miseráveis bons e ruins \\nnão são equilibradas, pois quando se é a favor de um, mesmo que \\nisso seja ne cessário para um bem maior e não é favorável aos \\npolíticos miseráveis odiosos é como o famoso ditado popular diz: \\n“cutucar a onça com vara curta”. No entanto, isso não é bom para \\no julgamento, pois torna -se exaustivo para a mente, para a sua \\nprópria vida e  para a vida de todos aqueles que o político mais \\nprecisa. Com isso, surge o sentimento de medo caótico de viver a \\nprópria vida que permeia a geração de miseráveis, líderes \\nmiseráveis e políticos miseráveis com depressão, ansiedade, \\nsíndrome do pânico, est afa e todos os ditos “maiores males do \\nséculo 21”.   \\n“A dificuldade de ter uma grande quantidade de miseráveis \\nodiosos como  empregados gera uma reação involuntária de \\nnegociar com o  inimigo devido ao próprio excesso monetário  \\nou pelo egocentrismo.”   \\nA gu la por esse dizeres acima mantinha os miseráveis \\nodiosos ocupados entre eles, pois não tinham inteligência \\nsuficiente para ocupar a liderança, assim um grande líder político \\nmiserável odioso não precisava preocupar -se com aqueles",
      "position": 98487,
      "chapter": 4,
      "page": 89,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.49523809523809,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 37.8,
        "avg_word_length": 4.984126984126984,
        "unique_word_ratio": 0.6613756613756614,
        "avg_paragraph_length": 189.0,
        "punctuation_density": 0.08994708994708994,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miseráveis",
          "políticos",
          "pois",
          "isso",
          "odiosos",
          "vida",
          "como",
          "própria",
          "todos",
          "aqueles",
          "político",
          "grande",
          "essas",
          "adversidades",
          "bons",
          "ruins",
          "equilibradas",
          "quando",
          "favor",
          "mesmo"
        ],
        "entities": [
          [
            "Essas",
            "GPE"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "político mais",
            "PERSON"
          ],
          [
            "de medo caótico de viver",
            "PERSON"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "21",
            "CARDINAL"
          ],
          [
            "reação involuntária de \\nnegociar",
            "PERSON"
          ],
          [
            "excesso monetário",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "acima mantinha",
            "PERSON"
          ]
        ],
        "readability_score": 79.60476190476192,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 125,
        "lexical_diversity": 0.6613756613756614
      },
      "preservation_score": 1.788086050863397e-05
    },
    {
      "id": 1,
      "text": "sujeitos considerados burr os, uma vez que quando ele chega a \\numa magnitude de ódio não precisa   \\n“lutar em uma frente de batalha” e, se isso ocorre, ele é muito \\nagressivo ao ponto de não ter ninguém a altura para combatê -lo. \\nPara atingir tal nível de ódio, precisa ter muita astúcia  e equilíbrio \\npara fazer “amigos” políticos miseráveis odiosos e astúcia para \\nincentivar outros miseráveis odiosos a “se matarem aos poucos \\npara uma grandeza material e monetária”. Assim, considera -se \\nque esses sujeitos têm a ganância pelo ódio, por isso o  preço para \\ncriar o caos é pequeno diante do ganho. É necessário ressaltar que \\ntodos os “ganhos” que são fruto de uma “facilidade” também são \\nconquistados pela mesma “facilidade” ...   \\nComo já foi mencionado, a conquista monetária é \\nnecessária, logo, para  se manter é necessário haver mais \\nconquistas monetárias, ocorrendo ganância involuntária para \\nfazer o bem, até porque para ter um maior valor monetário fica \\nlimitado, como diz o ditado popular “quem tem Porsche não \\nnegocia com quem tem Chevette”. Então, f azer o bem é também \\nfazer o mal, por isso percebemos que um político não precisa ser \\nganancioso e nem beneficiar -se de muitos luxos, pois ambos, \\nquando são muito exaltados, trazem o caos involuntários.",
      "position": 99760,
      "chapter": 4,
      "page": 90,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.830462519936205,
      "complexity_metrics": {
        "word_count": 209,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.833333333333336,
        "avg_word_length": 4.990430622009569,
        "unique_word_ratio": 0.6746411483253588,
        "avg_paragraph_length": 209.0,
        "punctuation_density": 0.11961722488038277,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ódio",
          "precisa",
          "isso",
          "fazer",
          "sujeitos",
          "quando",
          "muito",
          "astúcia",
          "miseráveis",
          "odiosos",
          "monetária",
          "ganância",
          "caos",
          "necessário",
          "facilidade",
          "também",
          "como",
          "quem",
          "considerados",
          "burr"
        ],
        "entities": [
          [
            "sujeitos considerados burr os",
            "ORG"
          ],
          [
            "quando ele",
            "PERSON"
          ],
          [
            "ponto de não",
            "ORG"
          ],
          [
            "altura para",
            "PERSON"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "astúcia  e",
            "PERSON"
          ],
          [
            "para fazer",
            "PERSON"
          ],
          [
            "astúcia para \\nincentivar outros miseráveis",
            "PERSON"
          ],
          [
            "matarem aos poucos \\npara uma grandeza",
            "PERSON"
          ],
          [
            "ganância pelo",
            "PERSON"
          ]
        ],
        "readability_score": 81.08620414673047,
        "semantic_density": 0,
        "word_count": 209,
        "unique_words": 141,
        "lexical_diversity": 0.6746411483253588
      },
      "preservation_score": 3.162089016263692e-05
    },
    {
      "id": 1,
      "text": "Além disso, é importante lembrar daquele político \\nmiserável que chegou à liderança pela confiança, que veio através \\nda semelhança de viver em caos. O sentimento caótico está \\natrelado a um poder que irá facilitar a administração de uma \\ncarreira na liderança  caótica. No entanto, cabe pontuar que não \\nsignifica que seja uma afeição natural em relação a confiar por ser \\nconfiável, e sim pela fadiga da dificuldade de viver, que gera \\nempatia pela semelhança de caos vivido. É impossível que \\npossam vir a ser felizes pelo caos, até porque nosso passado nos \\ncondena e essa condenação é viciante para aqueles que vivem em \\ncaos, esse vício os torna amigos devido a um regime antigo de \\ntrabalhar descontente, assim muitos se tornam amigos pela \\nnecessidade caótica de viver tend o o necessário.   \\nLogo, esses sujeitos que são favorecidos dessa forma \\nmuitas vezes se aproximam quando é preciso beneficiar -se para \\nser um melhor miserável caótico, assim mesmo que estiverem \\ndescontentes, são considerados descontentes confiáveis. É \\nnecessário ressaltar que não há fortaleza que resista quando se é \\nodiado pelos miseráveis, logo o político miserável tem a \\nnecessid ade de censurar os sujeitos que são contra o caos. Esse \\nsentimento, por sua vez, é capaz de conquistar a confiança",
      "position": 101156,
      "chapter": 4,
      "page": 91,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.25651872399445,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.428571428571427,
        "avg_word_length": 5.140776699029126,
        "unique_word_ratio": 0.6844660194174758,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.0970873786407767,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "pela",
          "miserável",
          "viver",
          "político",
          "liderança",
          "confiança",
          "semelhança",
          "sentimento",
          "caótico",
          "caótica",
          "esse",
          "amigos",
          "assim",
          "necessário",
          "logo",
          "sujeitos",
          "quando",
          "descontentes",
          "além"
        ],
        "entities": [
          [
            "da semelhança de viver",
            "PERSON"
          ],
          [
            "semelhança de caos vivido",
            "ORG"
          ],
          [
            "possam vir",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "essa condenação",
            "ORG"
          ],
          [
            "trabalhar descontente",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "resista quando",
            "PERSON"
          ],
          [
            "odiado pelos miseráveis",
            "PERSON"
          ]
        ],
        "readability_score": 83.74348127600555,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 141,
        "lexical_diversity": 0.6844660194174758
      },
      "preservation_score": 1.581044508131846e-05
    },
    {
      "id": 1,
      "text": "necessária para fazer a liderança justa, visto que aparenta merecer \\nos méritos, assim não há espaço para o medo de esconder -se e, \\nmuito menos , de omitir os seus atos, pois eles fazem o político \\nmiserável ganhar destaque.",
      "position": 102559,
      "chapter": 4,
      "page": 92,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.91538461538461,
      "complexity_metrics": {
        "word_count": 39,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 39.0,
        "avg_word_length": 4.717948717948718,
        "unique_word_ratio": 0.8974358974358975,
        "avg_paragraph_length": 39.0,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessária",
          "fazer",
          "liderança",
          "justa",
          "visto",
          "aparenta",
          "merecer",
          "méritos",
          "assim",
          "espaço",
          "medo",
          "esconder",
          "muito",
          "menos",
          "omitir",
          "seus",
          "atos",
          "pois",
          "eles",
          "fazem"
        ],
        "entities": [
          [
            "para fazer",
            "PERSON"
          ],
          [
            "para o medo de esconder -se e",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "ganhar destaque",
            "PERSON"
          ]
        ],
        "readability_score": 79.08461538461539,
        "semantic_density": 0,
        "word_count": 39,
        "unique_words": 35,
        "lexical_diversity": 0.8974358974358975
      },
      "preservation_score": 7.905222540659229e-07
    },
    {
      "id": 1,
      "text": "Capítulo 21   \\nO que convém a um político    \\nComo foi mencionado anteriormente, conquistar a \\nliderança através do sentimento é a forma mais difícil e longa, \\nporém a mai s fácil de se manter. Devido a isso, o trajeto para a \\nliderança só é admirável pela semelhança com a miséria. A \\nnecessidade de existir a miséria durante toda a existência humana \\nfoi exemplo de uma vida para ser um miserável que é a mesma \\nexistência da nece ssidade pela ganância humana, pois sem a \\nmiséria não existiria o luxo.   \\nEssa miséria que nós, miseráveis, nos identificamos é \\nsemelhante a dor vivida em histórias religiosas, filosóficas, \\nanalogias, metáforas. Os direcionamentos tornam -se exemplos \\npela do r vivida devido ao próprio viver, que se mantém pela \\nprópria miséria em, por exemplo, dar um dízimo com a esperança \\nde curar a sua dor. Muitos criam os maiores empreendimentos e \\nse alimentam da miséria, eles são tão numerosos que conseguem \\nalimentar um gra nde exército para combater a própria fome. Se \\nhouvesse uma distribuição menos gananciosa por parte dos \\npolíticos miseráveis que os lideram, muitos viveriam bem. No",
      "position": 103079,
      "chapter": 21,
      "page": 94,
      "segment_type": "page",
      "themes": {
        "filosofia": 75.0,
        "arte": 25.0
      },
      "difficulty": 27.935860655737706,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 22.875,
        "avg_word_length": 4.994535519125683,
        "unique_word_ratio": 0.7213114754098361,
        "avg_paragraph_length": 183.0,
        "punctuation_density": 0.11475409836065574,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miséria",
          "pela",
          "liderança",
          "devido",
          "existência",
          "humana",
          "exemplo",
          "miseráveis",
          "vivida",
          "própria",
          "muitos",
          "capítulo",
          "convém",
          "político",
          "como",
          "mencionado",
          "anteriormente",
          "conquistar",
          "através",
          "sentimento"
        ],
        "entities": [
          [
            "21",
            "CARDINAL"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "ganância humana",
            "PERSON"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "filosóficas",
            "DATE"
          ],
          [
            "própria miséria",
            "PERSON"
          ],
          [
            "se alimentam da miséria",
            "PERSON"
          ],
          [
            "viveriam bem",
            "PERSON"
          ]
        ],
        "readability_score": 87.0641393442623,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 132,
        "lexical_diversity": 0.7213114754098361
      },
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "id": 1,
      "text": "entanto, não sentem satisfação em tais façanhas para fazer os \\nmiseráveis serem humanos, pois  eles são os mesmos que os fazem \\nviver o luxo, e o não viver com o luxo, atitude que não condiz \\ncom a forma de ser líder político miserável.   \\nUm político que não conhece o tamanho da sua própria \\nliderança não saberá reconhecer e agir com todos aqueles que  \\nprecisam ser liderados, até quando verdadeiro amigo é, inimigo \\nde outro amigo também será. Quando quiser se beneficiar de \\noutro, será contra o que já foi dito antes. Afastar -se da guerra \\nsignifica se afastar do sentimento que o tornou líder, o que \\nocasion ará o afastamento da confiança conquistada. Quando digo \\nisso, não estou querendo me intrometer na liderança dos outros, \\nmas sinalizar que essa seria uma decisão desfavorável, não vivo a \\nliderança que você vive, porém vivo com os miseráveis \\ndesonestos e ing ratos, por isso sei que ambos podem ser \\noprimidos, até porque sua liderança nunca será tão grande que o \\npolítico não tenha tido outros semelhantes. Esses sujeitos, por sua \\nvez, necessitam ter uma maior consideração e ser mais justos \\ndevido à participação m ais enfática na trajetória da liderança \\npolítica. Além de todas as diferenças que existem de acordo com \\no tamanho da liderança, nesse crescimento há momentos em que",
      "position": 104355,
      "chapter": 4,
      "page": 95,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.0370249017038,
      "complexity_metrics": {
        "word_count": 218,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 31.142857142857142,
        "avg_word_length": 4.885321100917431,
        "unique_word_ratio": 0.6697247706422018,
        "avg_paragraph_length": 218.0,
        "punctuation_density": 0.10550458715596331,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "liderança",
          "político",
          "quando",
          "será",
          "miseráveis",
          "viver",
          "luxo",
          "líder",
          "tamanho",
          "amigo",
          "outro",
          "afastar",
          "isso",
          "outros",
          "vivo",
          "entanto",
          "sentem",
          "satisfação",
          "tais",
          "façanhas"
        ],
        "entities": [
          [
            "para fazer",
            "PERSON"
          ],
          [
            "serem humanos",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "até quando verdadeiro",
            "PERSON"
          ],
          [
            "de outro",
            "PERSON"
          ],
          [
            "também será",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "que",
            "CARDINAL"
          ]
        ],
        "readability_score": 82.9629750982962,
        "semantic_density": 0,
        "word_count": 218,
        "unique_words": 146,
        "lexical_diversity": 0.6697247706422018
      },
      "preservation_score": 1.8069080092935382e-05
    },
    {
      "id": 1,
      "text": "ocorre a necessidade de se envolver com pessoas que tiveram que \\nser conquistadas de uma for ma errada devido ao seu caráter.   \\n Nesse trajeto, podem ocorrer perdas importantes de \\npessoas dignas de confiança e, para se reestruturar, muitas vezes \\né necessário entrar no erro de conquistar a maioria através de uma \\nminoria que é agradada por meio da g anância, que é exemplo para \\nos miseráveis e que eles devem se esforçar para ter uma vida \\n“melhor”.    \\n“Querer ajudar logo o deixará associado a uma ganância que \\npoderá restringir a sua liderança.”   \\nAtravés dos fatos, percebemos que um político deve ter \\ncautela para fazer novas alianças com outros políticos miseráveis, \\nassim como a sua liderança teve um trajeto a do outro também, e \\na necessidade de saber limitar a outros grandes políticos \\nmiseráveis significa a ascensão da sua liderança.  Enxergar, \\nentender  e compreender a ordem dos aspectos e nunca fugir das \\nsituações inconvenientes é de suma importância para saber \\nconhecer o caráter dos inconvenientes e os tomar como aliados \\ndaqueles sujeitos de caráter menos prejudicial.",
      "position": 105777,
      "chapter": 4,
      "page": 96,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.14114285714286,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 5.137142857142857,
        "unique_word_ratio": 0.6685714285714286,
        "avg_paragraph_length": 175.0,
        "punctuation_density": 0.07428571428571429,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caráter",
          "miseráveis",
          "liderança",
          "necessidade",
          "pessoas",
          "trajeto",
          "através",
          "outros",
          "políticos",
          "como",
          "saber",
          "inconvenientes",
          "ocorre",
          "envolver",
          "tiveram",
          "conquistadas",
          "errada",
          "devido",
          "nesse",
          "podem"
        ],
        "entities": [
          [
            "ser conquistadas de uma",
            "ORG"
          ],
          [
            "ma errada devido",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "para se reestruturar",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "meio da g anância",
            "PERSON"
          ],
          [
            "devem se esforçar para",
            "PERSON"
          ],
          [
            "Querer",
            "ORG"
          ],
          [
            "deixará",
            "GPE"
          ]
        ],
        "readability_score": 80.95885714285714,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 117,
        "lexical_diversity": 0.6685714285714286
      },
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "id": 1,
      "text": "Além disso, um bom político deve  mostrar confiança e \\nafeto aos humanos dignos e confiáveis. Esses sujeitos são aqueles \\nque são considerados   \\n“fora da curva”, seja através do dom, seja através da \\ndeterminação. Quando reconhecer esses indivíduos, reconheça \\ntambém o que faz esses humanos serem “melhores e fora da \\ncurva”, pois eles exercem dignamente o seu viver miserável.   \\nO político que é querido por todos não é o melhor, e sim \\naquele que assemelha a sua necessidade a um contexto da sua \\nprópria liderança. Logo, percebemos que o bom polít ico é aquele \\nque escuta e analisa o melhor dentro daquilo que o fez ser líder.",
      "position": 106996,
      "chapter": 4,
      "page": 97,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.05188679245283,
      "complexity_metrics": {
        "word_count": 106,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 21.2,
        "avg_word_length": 4.839622641509434,
        "unique_word_ratio": 0.6981132075471698,
        "avg_paragraph_length": 106.0,
        "punctuation_density": 0.11320754716981132,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "esses",
          "político",
          "humanos",
          "fora",
          "curva",
          "seja",
          "através",
          "melhor",
          "aquele",
          "além",
          "disso",
          "deve",
          "mostrar",
          "confiança",
          "afeto",
          "dignos",
          "confiáveis",
          "sujeitos",
          "aqueles",
          "considerados"
        ],
        "entities": [
          [
            "mostrar confiança",
            "PERSON"
          ],
          [
            "aos humanos dignos e confiáveis",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "humanos serem",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "analisa o melhor",
            "ORG"
          ]
        ],
        "readability_score": 87.94811320754717,
        "semantic_density": 0,
        "word_count": 106,
        "unique_words": 74,
        "lexical_diversity": 0.6981132075471698
      },
      "preservation_score": 6.023026697645128e-06
    },
    {
      "id": 1,
      "text": "Capítulo 22   \\nAqueles que estão juntos   \\nA dificuldade de uma liderança não é só saber identificar \\ncomo ser um político, mas também saber instruir aqueles que são \\nliderados, pois esses sujeitos têm dificuldades de processar o \\ntrabalho a ser executado. Por muitas vezes, não são capazes de \\naprender , então atribuem a culpa de sua miséria a outros que nada \\nfizeram para a construção do cenário em que estão inseridos.  \\nEles, assim, acham perdão na religião, nos estudos, na academia, \\nnas drogas, no sexo e em tudo aquilo que pode ser uma fuga da \\nprópria v ida.    \\nA importância, para um político, resulta em observar \\naqueles que vivem próximos, pois são eles que mais podem te \\nprejudicar, uma vez que estão em maior número e têm mais \\nganância e confiança.   \\nDentro dessas importâncias é possível observar polític os \\nmiseráveis com três tipos de caráter: aqueles que entendem a vida \\npor si, outros que escutam e passam a informação e o último é \\n“Maria vai com as outras”, como expõe um ditado popular muito \\nconhecido. O primeiro é excelente, logo você sabe como agir com",
      "position": 107779,
      "chapter": 22,
      "page": 98,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.75996376811594,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.666666666666668,
        "avg_word_length": 4.755434782608695,
        "unique_word_ratio": 0.6956521739130435,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.125,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "aqueles",
          "estão",
          "como",
          "saber",
          "político",
          "pois",
          "outros",
          "eles",
          "observar",
          "mais",
          "capítulo",
          "juntos",
          "dificuldade",
          "liderança",
          "identificar",
          "também",
          "instruir",
          "liderados",
          "esses",
          "sujeitos"
        ],
        "entities": [
          [
            "22",
            "CARDINAL"
          ],
          [
            "mas também",
            "PERSON"
          ],
          [
            "então",
            "ORG"
          ],
          [
            "nada \\nfizeram para",
            "ORG"
          ],
          [
            "acham",
            "ORG"
          ],
          [
            "nas drogas",
            "PERSON"
          ],
          [
            "própria v ida",
            "PERSON"
          ],
          [
            "têm mais \\nganância",
            "ORG"
          ],
          [
            "Dentro",
            "LOC"
          ],
          [
            "Maria",
            "NORP"
          ]
        ],
        "readability_score": 83.24003623188406,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 128,
        "lexical_diversity": 0.6956521739130435
      },
      "preservation_score": 1.788086050863397e-05
    },
    {
      "id": 1,
      "text": "ele, o segundo torna se bom sabendo diferenciar aspectos \\npositivos e negativos em relação às informações que ele passa, e \\no terceiro é um peso morto, pois não tem caráter de bom uso.   \\nUm bom político percebe que, para fazer boas alianças, \\nnão deve ter o  pensamento centrado em si próprio. Logo, para ele \\nperceber a confiança de um futuro aliado, deve pensar sobre o \\ncontexto daquele sujeito em um tempo posterior. Esses sujeitos \\ntêm a capacidade de conhecer o bem e o mal que uma pessoa \\npossa fazer ou dizer.  Por outro lado, para conservar esse aliado, \\ndeve -se pensar na ganância dele de forma proporcional à \\nliderança atingida, até porque o sentimento de ser honrado e rico \\nmuitas vezes os obriga a participarem da evolução de um grande \\npolítico.  Cabe ressaltar,  nesse sentido, que conservar as \\nnecessidades de um líder significa conservar também a vivência \\nno luxo para todos aqueles que olham para o representante como \\nexemplo, já que o próprio luxo é exemplo para aqueles que \\nusufruem desses benefícios.",
      "position": 109024,
      "chapter": 4,
      "page": 99,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.791472868217056,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 28.666666666666668,
        "avg_word_length": 4.8604651162790695,
        "unique_word_ratio": 0.7093023255813954,
        "avg_paragraph_length": 172.0,
        "punctuation_density": 0.11046511627906977,
        "line_break_count": 16,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "deve",
          "conservar",
          "político",
          "fazer",
          "próprio",
          "aliado",
          "pensar",
          "luxo",
          "aqueles",
          "exemplo",
          "segundo",
          "torna",
          "sabendo",
          "diferenciar",
          "aspectos",
          "positivos",
          "negativos",
          "relação",
          "informações",
          "passa"
        ],
        "entities": [
          [
            "para fazer",
            "PERSON"
          ],
          [
            "boas",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "para ele \\n",
            "PERSON"
          ],
          [
            "possa fazer",
            "PERSON"
          ],
          [
            "Por outro lado",
            "PERSON"
          ],
          [
            "ganância dele de forma",
            "PERSON"
          ],
          [
            "de ser honrado e",
            "PERSON"
          ],
          [
            "rico",
            "LAW"
          ],
          [
            "significa",
            "PERSON"
          ]
        ],
        "readability_score": 84.20852713178294,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 122,
        "lexical_diversity": 0.7093023255813954
      },
      "preservation_score": 1.2046053395290256e-05
    },
    {
      "id": 1,
      "text": "Capítulo 23   \\nAfastar aqueles miseráveis gananciosos   \\n O político que atingiu uma liderança com grandes valores \\nmonetários terá dificuldades para manter a confiança daqueles \\nque chama de “amigos”, pois essa palavra vem com um peso de \\nsentimento atrelado à admiração de valor familiar. Logo, esse \\nsentimento o de ixa cego diante de sua própria interpretação sobre \\na avaliação acerca do que é certo para um bem maior ou um bem \\nsó para o seu “amigo”. Lembrando que estou me referindo \\nàqueles que sentem inveja das coisas monetárias e das aparências, \\npois esses elementos os fazem se iludir facilmente devido à \\nprópria forma de evoluir a vida.   \\nPorém, se houver a necessidade de limitar as ações \\ndesses “amigos”, nunca se esqueça que as ofensas geradas, por \\nmais que possam ser verdades, não devem te incomodar, até \\nporque esse  sentimento traz desconfiança daqueles que confiam \\nem você. Se for inevitável, não deixe que sejam maiores que o \\nseu caráter, pois ele é composto de erros confiáveis que foram \\nobtidos no trajeto. Logo, se a ofensa for de um errar do próprio \\ncaráter, não te rá forças para afetar um grande político, até",
      "position": 110184,
      "chapter": 23,
      "page": 100,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.22936507936508,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 31.5,
        "avg_word_length": 4.931216931216931,
        "unique_word_ratio": 0.6984126984126984,
        "avg_paragraph_length": 189.0,
        "punctuation_density": 0.09523809523809523,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "sentimento",
          "político",
          "daqueles",
          "amigos",
          "logo",
          "esse",
          "própria",
          "caráter",
          "capítulo",
          "afastar",
          "aqueles",
          "miseráveis",
          "gananciosos",
          "atingiu",
          "liderança",
          "grandes",
          "valores",
          "monetários",
          "terá"
        ],
        "entities": [
          [
            "23",
            "CARDINAL"
          ],
          [
            "gananciosos",
            "PERSON"
          ],
          [
            "para manter",
            "PERSON"
          ],
          [
            "que chama de “amigos",
            "PERSON"
          ],
          [
            "admiração de valor",
            "ORG"
          ],
          [
            "diante de sua própria",
            "PERSON"
          ],
          [
            "certo",
            "NORP"
          ],
          [
            "Lembrando",
            "ORG"
          ],
          [
            "própria forma de evoluir",
            "PERSON"
          ],
          [
            "Porém",
            "PERSON"
          ]
        ],
        "readability_score": 82.77063492063492,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 132,
        "lexical_diversity": 0.6984126984126984
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "porque esses mesmos erros podem ser os seus livramentos de \\nalgo pior no futuro. Assim, isso faz com que as suas palavras \\nsejam mais aceitas devido à existência de uma vida de livre \\nassunto com nada para esconde r.   \\n“A omissão de pronunciar -se diante de uma necessidade significa \\na falta de sentimento perante o incômodo de quem precisa ser  \\nliderado.”   \\nUm político, portanto, sempre deve se aconselhar \\ndaqueles que ele confia quando é necessário,  antes  que \\noutros  queiram aconselhar sem saber aconselhar e, se isso vier \\nacontecer, deve antecipar -se e perguntar antes que seja \\naconselhado. Logo, enfatizare mos a necessidade de ser um \\nouvinte paciente e atento, essas qualidades juntas são bem -vistas \\npelos humanos, além de servirem como bons aprendizados para \\nlimitar aqueles que precisam ser limitados.   \\nConversar com todos aqueles que são próximos para \\nconseg uir liderar melhor significa o aprendizado e a necessidade \\nde reconhecer as suas próprias falhas e as falhas de quem está \\npróximo. A ausência do diálogo, por outro lado, significa a \\ndecadência de manter -se na liderança, pois ele é capaz de",
      "position": 111488,
      "chapter": 5,
      "page": 101,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 29.526519337016573,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 25.857142857142858,
        "avg_word_length": 5.088397790055248,
        "unique_word_ratio": 0.7071823204419889,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.09944751381215469,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "significa",
          "aconselhar",
          "isso",
          "suas",
          "quem",
          "deve",
          "antes",
          "aqueles",
          "falhas",
          "porque",
          "esses",
          "mesmos",
          "erros",
          "podem",
          "seus",
          "livramentos",
          "algo",
          "pior",
          "futuro"
        ],
        "entities": [
          [
            "mesmos erros",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "sejam mais aceitas",
            "PERSON"
          ],
          [
            "existência de uma vida de livre",
            "ORG"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "r.",
            "NORP"
          ],
          [
            "incômodo de quem",
            "PERSON"
          ],
          [
            "portanto",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "queiram aconselhar",
            "PERSON"
          ]
        ],
        "readability_score": 85.54490923441199,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 128,
        "lexical_diversity": 0.7071823204419889
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "proporcionar não  só o ensino, mas também o aprendizado, \\ninclusive de outros grandes políticos.   \\n“Os bons conselhos, venham de onde vierem, devem nascer do \\ncaráter do político, e não do  \\ncaráter daqueles que dão bons conselhos...”   \\nAssim, conclui -se que, através das pala vras, muitos \\nconquistam o direito de serem grandes políticos.  Desse modo, \\nsaber se comunicar em comum com todos os liderados faz com \\nque eles compreendam sua ideia e possam vê -lo como uma \\nfigura grande. Há pensamentos que só o líder terá.    \\nDessa maneir a, entende -se que chegamos a uma conclusão \\nimpossível de ser realizada que é de conversar, compreender e ter \\nconfiança em todos aqueles que um grande líder político precisa.",
      "position": 112735,
      "chapter": 5,
      "page": 102,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.252586206896552,
      "complexity_metrics": {
        "word_count": 116,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 19.333333333333332,
        "avg_word_length": 5.008620689655173,
        "unique_word_ratio": 0.7586206896551724,
        "avg_paragraph_length": 116.0,
        "punctuation_density": 0.16379310344827586,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "grandes",
          "políticos",
          "bons",
          "conselhos",
          "caráter",
          "político",
          "todos",
          "grande",
          "líder",
          "proporcionar",
          "ensino",
          "também",
          "aprendizado",
          "inclusive",
          "outros",
          "venham",
          "onde",
          "vierem",
          "devem",
          "nascer"
        ],
        "entities": [
          [
            "proporcionar não  só",
            "PERSON"
          ],
          [
            "mas também",
            "PERSON"
          ],
          [
            "aprendizado",
            "GPE"
          ],
          [
            "venham de onde vierem",
            "PERSON"
          ],
          [
            "político",
            "PERSON"
          ],
          [
            "Assim",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Dessa",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 88.83074712643678,
        "semantic_density": 0,
        "word_count": 116,
        "unique_words": 88,
        "lexical_diversity": 0.7586206896551724
      },
      "preservation_score": 1.0841448055761226e-05
    },
    {
      "id": 1,
      "text": "Capítulo 24   \\nA derrota de um político   \\nManter uma liderança em espaços em que há muitas diferenças \\nentre as idades tem benefícios e malefícios, isso depende do \\npróprio líder.   \\nO novo político que tem a aparência de um político velho \\ntorna -se mais aceito não por ser b om político, e sim pela sua \\naparência ser de um político miserável, pois eles são cheios de \\nvícios de um viver preconceituoso evolutivo do próprio sistema. \\nEsse sistema que, antes, era recriminado é visto como virtuoso, \\nporque os miseráveis só vivem de um presente que é fruto de um \\npassado muito pior. Isso faz com que os miseráveis enxerguem os \\npolíticos miseráveis velhos como uma solução melhor do que \\noutros mais novos, devido ao conforto visual e audível \\npreconceituosos que estão relacionados à aparência das roupas, \\ncabelo, cor, sexo, forma de falar, forma de gesticular, lugar onde \\nmora, valor aquisitivo, família tradicional e muitas outras formas \\nde imaginar que aquilo é o melhor para ser político.   \\nAquele que lidera um grupo familiar sofre com a \\ndificul dade da confiança quando tem um alto poder aquisitivo e,",
      "position": 113745,
      "chapter": 24,
      "page": 104,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.87717391304348,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 36.8,
        "avg_word_length": 4.923913043478261,
        "unique_word_ratio": 0.7119565217391305,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.10869565217391304,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "político",
          "aparência",
          "miseráveis",
          "muitas",
          "isso",
          "próprio",
          "mais",
          "sistema",
          "como",
          "melhor",
          "forma",
          "aquisitivo",
          "capítulo",
          "derrota",
          "manter",
          "liderança",
          "espaços",
          "diferenças",
          "entre",
          "idades"
        ],
        "entities": [
          [
            "24",
            "CARDINAL"
          ],
          [
            "Manter",
            "PERSON"
          ],
          [
            "mais aceito não",
            "PERSON"
          ],
          [
            "aparência ser de um",
            "PERSON"
          ],
          [
            "muito pior",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "outros mais novos",
            "PERSON"
          ],
          [
            "aparência das roupas",
            "PERSON"
          ],
          [
            "cor",
            "ORG"
          ]
        ],
        "readability_score": 80.12282608695652,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 131,
        "lexical_diversity": 0.7119565217391305
      },
      "preservation_score": 1.5019922827252538e-05
    },
    {
      "id": 1,
      "text": "quando se têm essa herança aquisitiva e perde, se nunca viveu na \\nmiséria, a aparência de miserável será o fator que irá motivar a \\nsua grande histeria. Como essas situações nunca foram sentidas e \\nvivenciadas antes, provavelmente serão a sua ruína, pois para \\ncontrolar os nossos instintos primitivos ocorre a necessidade de \\nentender aquilo que o miserável vive, a realidade que, por muitas \\nvezes, causa mortes ou suicídios. Por outro lado, aqueles que \\nlideram pelo dinheiro sofrem para manter a ganância, temos \\naqueles que sofrem com a mão de obra de um amigo que pensa \\nque é melhor do que realmente é, tornando prejudicial para se \\nmanter dentro do seu entorno, logo acarretando a falta de \\nsabedoria para analisar  aqueles que são dignos de confiança.   \\nOs políticos miseráveis egocêntricos nunca pensam que o \\namanhã pode representar a mesma realidade do dia atual em que \\nse vive, pensam que os dias sempre vão ser pacíficos, acreditam \\nque “as merdas cagadas não voltam  ao rabo, porém essas merdas \\ndeixam rastros e esses rastros são fedorentos e de fácil acesso” \\ndevido ao próprio modo de viver com uma aparência luxuosa. \\nMuitas vezes, cometem atitudes perigosas e, em alguns momento, \\ncolocam -se em posições de divindade. No entanto, é necessário \\nenfatizar o famoso ditado popular “as aparências enganam”.",
      "position": 115017,
      "chapter": 5,
      "page": 105,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.358566978193146,
      "complexity_metrics": {
        "word_count": 214,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 35.666666666666664,
        "avg_word_length": 5.08411214953271,
        "unique_word_ratio": 0.6962616822429907,
        "avg_paragraph_length": 214.0,
        "punctuation_density": 0.11214953271028037,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nunca",
          "aqueles",
          "aparência",
          "miserável",
          "essas",
          "vive",
          "realidade",
          "muitas",
          "vezes",
          "sofrem",
          "manter",
          "pensam",
          "merdas",
          "rastros",
          "quando",
          "essa",
          "herança",
          "aquisitiva",
          "perde",
          "viveu"
        ],
        "entities": [
          [
            "quando se",
            "PERSON"
          ],
          [
            "têm essa herança aquisitiva e perde",
            "ORG"
          ],
          [
            "lideram pelo dinheiro",
            "PERSON"
          ],
          [
            "sofrem para manter",
            "PERSON"
          ],
          [
            "para analisar  aqueles",
            "PERSON"
          ],
          [
            "egocêntricos",
            "CARDINAL"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "merdas cagadas",
            "ORG"
          ],
          [
            "aparência luxuosa",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 80.64143302180685,
        "semantic_density": 0,
        "word_count": 214,
        "unique_words": 149,
        "lexical_diversity": 0.6962616822429907
      },
      "preservation_score": 2.1833471778963585e-05
    },
    {
      "id": 1,
      "text": "Assim, esse cenário cria uma falsa sensação de poder para os \\nmiseráveis desesperados e eles não percebem as boas, certas e \\nduradouras ações quando um grande líder político tem  caráter \\nincontestável de uma aceitação territorial.",
      "position": 116459,
      "chapter": 5,
      "page": 106,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.15428571428571,
      "complexity_metrics": {
        "word_count": 35,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 5.514285714285714,
        "unique_word_ratio": 0.9142857142857143,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.08571428571428572,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "esse",
          "cenário",
          "cria",
          "falsa",
          "sensação",
          "poder",
          "miseráveis",
          "desesperados",
          "eles",
          "percebem",
          "boas",
          "certas",
          "duradouras",
          "ações",
          "quando",
          "grande",
          "líder",
          "político",
          "caráter"
        ],
        "entities": [
          [
            "ações quando",
            "PERSON"
          ]
        ],
        "readability_score": 80.84571428571428,
        "semantic_density": 0,
        "word_count": 35,
        "unique_words": 32,
        "lexical_diversity": 0.9142857142857143
      },
      "preservation_score": 3.387952517425383e-07
    },
    {
      "id": 1,
      "text": "Capítulo 25    \\nQuanto um político pode ser feliz   \\nUm líder nunca pode contar com o caso do acaso, pois \\nqualquer ação ruim que possa acontecer no futuro está atrelada à \\nfalta de sabedoria de um grande político em não calcular os \\nmovimentos a serem observados antes de acontecer. Isso porque, \\ntoda liderança é conquistada a partir da sua própria sabedoria \\ndessa figura em ser o que tinha que ser e estar no lugar certo. \\nLogo, a perda da confiança significa a perda do seu próprio \\njulgamento em ser o político que deveria ser, por estar onde está, \\nmas nunca podemos  deixar de pensar que todos nós somos feitos \\nde “carne e osso” e isso nos motiva a realizar “ações carnais” \\ndesde a luxúria , a ganância, a ostentação, a motivação, o amor, o \\nsexo, os momentos de felicidades e de tristezas, as emoções, o \\nafeto e a liberdad e arbitrária limitada.     \\nOs excessos de regras se tornam visuais e um político não \\npode ser feliz visualmente falando, pois é necessário ter um estilo \\nde vida de acordo com a própria aparência.    \\n“Aqueles que julgam a todos pela forma de viver são \\nsujei tos que não vivem.”",
      "position": 116956,
      "chapter": 25,
      "page": 108,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.77738095238095,
      "complexity_metrics": {
        "word_count": 196,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.666666666666664,
        "avg_word_length": 4.535714285714286,
        "unique_word_ratio": 0.6530612244897959,
        "avg_paragraph_length": 196.0,
        "punctuation_density": 0.09693877551020408,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "político",
          "pode",
          "feliz",
          "nunca",
          "pois",
          "acontecer",
          "está",
          "sabedoria",
          "isso",
          "própria",
          "perda",
          "todos",
          "capítulo",
          "quanto",
          "líder",
          "contar",
          "caso",
          "acaso",
          "qualquer",
          "ação"
        ],
        "entities": [
          [
            "25    \\n",
            "DATE"
          ],
          [
            "qualquer ação ruim que",
            "PERSON"
          ],
          [
            "falta de sabedoria de",
            "ORG"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "ser o que",
            "ORG"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "significa",
            "PERSON"
          ],
          [
            "deixar de pensar",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "ações carnais",
            "PERSON"
          ]
        ],
        "readability_score": 82.30595238095239,
        "semantic_density": 0,
        "word_count": 196,
        "unique_words": 128,
        "lexical_diversity": 0.6530612244897959
      },
      "preservation_score": 1.788086050863397e-05
    },
    {
      "id": 1,
      "text": "Um grande líder político tem que ser exemplo para a \\nmaioria e ser exemplo para a maioria significa limitar o seu \\npróprio viver que, muitas vezes, é incoerente com a maioria. No \\nentanto, são essas ações incoerentes que, muitas vezes,  faziam -no \\nfeliz em certos momentos da vida , então controlar esses \\nmomentos é necessário para ser um grande líder político.  Cabe \\nressaltar que essas mudanças não podem alterar o seu caráter, pois \\nisso resulta, segundo eu creio pelas características expos tas, em \\num político que queira se dar um luxo de viver alguns prazeres \\nprazerosos e isso não pode ocorrer, pois dar -se de presente esse \\nmomento é “contar com a sorte no azar”.   \\n“Assim como os artistas que não se atualizam perdem a fama, um \\npolítico que não se adapta  \\nà evolução retarda a evolução.”   \\nTodos os tipos de líderes são bons para aqueles que são \\nbeneficiados, desde um político assassino a um político bondoso, \\nambos têm valores de liderança e de caráter semelhantes aos seus \\nliderados.  Desse modo, um bom político é igual a um artista, o \\nvalor da liderança é igual ao valor do sentimento da quantidade \\nde miseráveis que o seguem.",
      "position": 118231,
      "chapter": 5,
      "page": 109,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.84472789115647,
      "complexity_metrics": {
        "word_count": 196,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.666666666666664,
        "avg_word_length": 4.760204081632653,
        "unique_word_ratio": 0.6275510204081632,
        "avg_paragraph_length": 196.0,
        "punctuation_density": 0.10714285714285714,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "político",
          "maioria",
          "grande",
          "líder",
          "exemplo",
          "viver",
          "muitas",
          "vezes",
          "essas",
          "momentos",
          "caráter",
          "pois",
          "isso",
          "evolução",
          "liderança",
          "igual",
          "valor",
          "significa",
          "limitar",
          "próprio"
        ],
        "entities": [
          [
            "significa limitar",
            "PERSON"
          ],
          [
            "faziam -no \\nfeliz",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "político",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "segundo eu creio",
            "ORG"
          ],
          [
            "características",
            "GPE"
          ],
          [
            "aos seus",
            "PERSON"
          ]
        ],
        "readability_score": 82.23860544217688,
        "semantic_density": 0,
        "word_count": 196,
        "unique_words": 123,
        "lexical_diversity": 0.6275510204081632
      },
      "preservation_score": 1.931132934932469e-05
    },
    {
      "id": 1,
      "text": "Um político sábio consegue ser feliz naquil o que o conduz \\nem fazer uma ótima liderança, pois essa condição sempre irá o \\nlevar para aquilo que pode transformá -lo em um líder maior, \\ncomo um presidente, por exemplo. Contudo, para atingir esse \\nobjetivo, é necessário considerar que as ganâncias e a conf iança \\nprocedem de diversas formas: algumas em momentos de caos, \\noutras em situações de felicidade, de agressividade, de \\nsagacidade. Somos diferentes, o que pode fazer com que um \\nindivíduo seja contrário ao outro, pois cada um tem seu estilo de \\nvida, mas to dos podem alcançar os seus objetivos de diferentes \\nmodos.   \\nConseguir fazer uma liderança de pensamentos mútuos \\nem concordância para de fazer o bem significa que alcançar os \\nobjetivos de um representa a conquista do outro também, visto \\nque têm os mesmos ob jetivos. Assim, considera -se que “um joga \\nde lateral e o outro de atacante, porém todos querem fazer o \\nmesmo gol”. Muitas vezes, a qualidade de um é o defeito do \\noutro, assim podem evoluir juntos, até porque chegar a uma \\ngrande posição política em concordâ ncia com o outro grande \\npolítico requer conversar, debater, criticar, aceitar, adaptar. Essas",
      "position": 119506,
      "chapter": 5,
      "page": 110,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.48469387755102,
      "complexity_metrics": {
        "word_count": 196,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.0,
        "avg_word_length": 4.948979591836735,
        "unique_word_ratio": 0.673469387755102,
        "avg_paragraph_length": 196.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "outro",
          "político",
          "liderança",
          "pois",
          "pode",
          "diferentes",
          "podem",
          "alcançar",
          "objetivos",
          "assim",
          "grande",
          "sábio",
          "consegue",
          "feliz",
          "naquil",
          "conduz",
          "ótima",
          "essa",
          "condição"
        ],
        "entities": [
          [
            "feliz naquil",
            "PERSON"
          ],
          [
            "sempre irá o",
            "PERSON"
          ],
          [
            "Contudo",
            "PERSON"
          ],
          [
            "necessário considerar que",
            "ORG"
          ],
          [
            "conf iança \\nprocedem de diversas",
            "ORG"
          ],
          [
            "objetivos",
            "CARDINAL"
          ],
          [
            "Conseguir",
            "PERSON"
          ],
          [
            "outro também",
            "PERSON"
          ],
          [
            "mesmos ob jetivos",
            "PERSON"
          ],
          [
            "outro de atacante",
            "PERSON"
          ]
        ],
        "readability_score": 84.51530612244898,
        "semantic_density": 0,
        "word_count": 196,
        "unique_words": 132,
        "lexical_diversity": 0.673469387755102
      },
      "preservation_score": 2.2887501451051485e-05
    },
    {
      "id": 1,
      "text": "são atitudes muito valorizadas e que fazem com que ambos \\npossam evoluir juntos para se tornarem gigantes.   \\n “O político acomodado torna -se estagnado e medíocre. Logo, o \\npolítico que não sabe evoluir e instruir os liderados que tinham \\npotencial  faz com que eles também  se tornem  medíocres  e \\nacomodados.”    \\nPor isso, o político cauteloso deve saber limitar.  Caso não \\nsaiba, certamente cairá em desgraça como consequência. Se ele \\nconseguir acompanhar a evolução de acordo com o necessário, \\nconsiderando o que está vivendo no momento, a sua liderança \\nnunca deixará  de ser grandiosa, pois ela será atemporal.   \\n“A ruína de um político é a falta da percepção do seu próprio \\njulgamento em limitar o  \\nincômodo futuro.”   \\nUm presidente também é humano, logo nenhum humano \\nque seja, não poderá negar as pessoas que foram cria das ao seu \\nlado. Negar a sua origem gera manifestações de injúrias pela \\nnossa própria de negação da construção do caráter. Esses \\nacontecimentos, nos tempos que foram necessários, aqueles que \\nestavam ao nosso lado foram as pessoas que não deixaram nós",
      "position": 120809,
      "chapter": 5,
      "page": 111,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.32586206896552,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 17.4,
        "avg_word_length": 5.086206896551724,
        "unique_word_ratio": 0.735632183908046,
        "avg_paragraph_length": 174.0,
        "punctuation_density": 0.10919540229885058,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "político",
          "evoluir",
          "logo",
          "também",
          "limitar",
          "humano",
          "negar",
          "pessoas",
          "lado",
          "atitudes",
          "muito",
          "valorizadas",
          "fazem",
          "ambos",
          "possam",
          "juntos",
          "tornarem",
          "gigantes",
          "acomodado",
          "torna"
        ],
        "entities": [
          [
            "são",
            "ORG"
          ],
          [
            "muito valorizadas e",
            "PERSON"
          ],
          [
            "possam evoluir juntos",
            "PERSON"
          ],
          [
            "para se tornarem gigantes",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "se tornem  medíocres  ",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "deixará  de ser grandiosa",
            "PERSON"
          ],
          [
            "ela será",
            "PERSON"
          ]
        ],
        "readability_score": 89.77413793103449,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 128,
        "lexical_diversity": 0.735632183908046
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "sermo s medíocres. Assim, é necessário que jamais deixemos de \\nsaber a natureza do nosso caráter, até porque não limitar a \\nincoerência diante do nosso caráter significa falta de \\ninterpretação da nossa futura ruína, pois o nosso presente já \\nestamos vivendo devido ao nosso passado e ele nos guia para \\num futuro melhor.   \\n “Assim, uma líder que não enxerga esse processo não sabe como \\num peão se movimenta no xadrez.”   \\nAtravés de tudo que foi mencionado neste capítulo, \\nconsidera -se que a felicidade é igual um adolescen te, mescla \\nmuito amor e ódio com tanta energia que, muitas vezes, não \\ncontrola. Os momentos de “indecências” apropriadas para jovens, \\npor exemplo, não são dignos para um grande líder político, pois \\nsão vividos com muita liberdade, menos regras e não são \\ncautelosos. Assim, essa audácia de ser feliz pode te dominar.",
      "position": 122020,
      "chapter": 5,
      "page": 112,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.160191846522782,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 23.166666666666668,
        "avg_word_length": 4.9784172661870505,
        "unique_word_ratio": 0.7697841726618705,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.1366906474820144,
        "line_break_count": 14,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "assim",
          "caráter",
          "pois",
          "líder",
          "sermo",
          "medíocres",
          "necessário",
          "jamais",
          "deixemos",
          "saber",
          "natureza",
          "porque",
          "limitar",
          "incoerência",
          "diante",
          "significa",
          "falta",
          "interpretação",
          "nossa"
        ],
        "entities": [
          [
            "sermo s",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "jamais deixemos de \\n",
            "PERSON"
          ],
          [
            "nosso caráter",
            "PERSON"
          ],
          [
            "caráter significa falta de \\n",
            "PERSON"
          ],
          [
            "já \\nestamos vivendo devido ao",
            "PERSON"
          ],
          [
            "peão se movimenta",
            "PERSON"
          ],
          [
            "Através de tudo que",
            "ORG"
          ],
          [
            "muito amor",
            "PERSON"
          ]
        ],
        "readability_score": 86.92314148681055,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 107,
        "lexical_diversity": 0.7697841726618705
      },
      "preservation_score": 1.2648356065054767e-05
    },
    {
      "id": 1,
      "text": "Capítulo 26   \\nLiberar os miseráveis da miséria   \\nPensando comigo mesmo, é necessário liderar um país, \\nsenhor presidente, pois como vimos, ao decorrer de todo este \\nlivro, “pequenos” líderes sofrem em pequenos territórios para \\nconseguir liderar.  Em pequenas escalas de humanos há muitas \\ndiferenças, sejam e las raciais, culturais, amor, sentimento, \\ndinheiro, idade e todos aqueles incômodos que a sigla do sinal de \\n+ que consta na bandeira LGBTQ resume da melhor forma, visto \\nque indica que é essencial aceitar a todos, porém, como vimos, é \\nimpossível ser preside nte para todos. Logo, vejo a necessidade de \\nassumir todos os riscos e ser digno diante da nossa própria \\ndignidade.   \\n“Vamos criar possibilidades imaginárias, se todos nós tivéssemos \\noportunidades de viver em uma nova organização, em que todos \\nos humanos fo ssem feitos de honra e fossem  felizes, todos iam \\nconcorrer a tantas circunstâncias de felicidade que a concorrência  \\npela dor seria maior.”    \\nComo dito ao decorrer de todo este livro, se todos nós \\nvivêssemos no luxo, o emprego miserável seria exaltado.",
      "position": 123165,
      "chapter": 26,
      "page": 114,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.67588235294117,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 34.0,
        "avg_word_length": 5.252941176470588,
        "unique_word_ratio": 0.7352941176470589,
        "avg_paragraph_length": 170.0,
        "punctuation_density": 0.15294117647058825,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "como",
          "liderar",
          "vimos",
          "decorrer",
          "todo",
          "este",
          "livro",
          "pequenos",
          "humanos",
          "seria",
          "capítulo",
          "liberar",
          "miseráveis",
          "miséria",
          "pensando",
          "comigo",
          "mesmo",
          "necessário",
          "país"
        ],
        "entities": [
          [
            "26",
            "CARDINAL"
          ],
          [
            "Pensando",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "pois como vimos",
            "ORG"
          ],
          [
            "las raciais",
            "GPE"
          ],
          [
            "culturais",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "vejo",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 81.42411764705882,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 125,
        "lexical_diversity": 0.7352941176470589
      },
      "preservation_score": 2.145703261036077e-05
    },
    {
      "id": 1,
      "text": "Vejamos o exemplo da Europa e dos Estados Unidos, todos esses \\nlugares estão com escassez de mão de obra, pois todos aqueles \\nque são considerados bons pais são aqueles que querem o melhor \\npara os seus filhos.   \\n“Os melhores empregos que podemos imaginar como \\nprofissões dignas para os nossos  filhos  trabalharem \\nsignificam  o afastamento de algumas ações e o abandono do \\nsistema que vivemos desde quando o primeiro  \\nmovimento surgiu.”   \\nA forma de alguns líderes chegarem à presidência não \\nocorre através da sorte , pois não há sorte quando se chega a essa \\nliderança a qual foi designada. Logo, concluo que a perda do \\neleitorado ocorre devido ao seu próprio erro perante o próprio \\ntrajeto, pois a liderança de uns não é mais justa nem mais do que \\noutra.  Essas liderança s que sabem limitar e ser justas quando \\nnecessário são fruto de grandes líderes de caráter forte e, dentro \\nde todas essas lideranças, temos uma tendência de termos um \\nconjunto de pessoas semelhantes a um viver em   \\n“fazer o gol”, uns são ruins, outros são bons. Isso ocorre devido à \\nnecessidade de nos adaptarmos e evoluirmos, um orientando o",
      "position": 124415,
      "chapter": 5,
      "page": 115,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.358245614035084,
      "complexity_metrics": {
        "word_count": 190,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 31.666666666666668,
        "avg_word_length": 4.8052631578947365,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 190.0,
        "punctuation_density": 0.07894736842105263,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "quando",
          "ocorre",
          "liderança",
          "todos",
          "aqueles",
          "bons",
          "filhos",
          "líderes",
          "sorte",
          "devido",
          "próprio",
          "mais",
          "essas",
          "vejamos",
          "exemplo",
          "europa",
          "estados",
          "unidos",
          "esses"
        ],
        "entities": [
          [
            "Vejamos",
            "PERSON"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "que querem",
            "PERSON"
          ],
          [
            "melhor",
            "GPE"
          ],
          [
            "afastamento de algumas ações",
            "ORG"
          ],
          [
            "chegarem à",
            "PERSON"
          ],
          [
            "presidência não",
            "PERSON"
          ]
        ],
        "readability_score": 82.72508771929824,
        "semantic_density": 0,
        "word_count": 190,
        "unique_words": 130,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "outro, ouvindo e falando, conversando e debatendo, estudando e \\nvivendo, trabalhando e descansando, amando e odiando, \\nlimitando e sabendo ser limitado, feliz e triste, no  caos e na paz.   \\n“Assim, irei concluir que nenhum homem é capaz de ser \\npresidente.”   \\nEsse mesmo sem ter uma noção do que cada eleitorado \\nprecisa, pois uns são a favor da guerra, outros da paz, uns do amor, \\noutros do ódio, nunca estão em concordância. As sim, isso me faz \\nconcluir que, se for para errar, o erro deve beneficiar a miséria, \\nnão por pena, e sim pela necessidade de ter a maioria ao seu lado. \\nSe, por acaso, tiver dúvidas sobre como deve agir, aja em \\ncoerência ao caráter que te levou à presidência , pois ele já \\nproporcionou um direcionamento, por isso sempre será o seu \\nmaior trunfo para ser o principal líder de uma nação.",
      "position": 125664,
      "chapter": 5,
      "page": 116,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.87708333333333,
      "complexity_metrics": {
        "word_count": 144,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 28.8,
        "avg_word_length": 4.590277777777778,
        "unique_word_ratio": 0.7569444444444444,
        "avg_paragraph_length": 144.0,
        "punctuation_density": 0.2013888888888889,
        "line_break_count": 13,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "concluir",
          "pois",
          "outros",
          "isso",
          "deve",
          "outro",
          "ouvindo",
          "falando",
          "conversando",
          "debatendo",
          "estudando",
          "vivendo",
          "trabalhando",
          "descansando",
          "amando",
          "odiando",
          "limitando",
          "sabendo",
          "limitado",
          "feliz"
        ],
        "entities": [
          [
            "outro",
            "ORG"
          ],
          [
            "falando",
            "GPE"
          ],
          [
            "sabendo ser limitado",
            "ORG"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "nenhum",
            "ORG"
          ],
          [
            "cada",
            "GPE"
          ],
          [
            "eleitorado",
            "GPE"
          ],
          [
            "outros da paz",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ]
        ],
        "readability_score": 84.22291666666666,
        "semantic_density": 0,
        "word_count": 144,
        "unique_words": 109,
        "lexical_diversity": 0.7569444444444444
      },
      "preservation_score": 1.5170498494693666e-05
    },
    {
      "id": 1,
      "text": "Carta para o presidente   \\n  \\n“Como vimos, ao decorrer do livro, vossa excelência, o nosso \\nlíder da nação, chegamos a uma conclusão inconclusiva”   \\n  Logo, percebemos que movimentar -se de um para com o outro \\né impossível. Todos nós, inclusive você líder da nação, temos \\nDNA diferentes, temos criações diferentes, trajetos diferentes, \\nganâncias diferentes, empatias diferentes, fazer sexo diferente, \\nolhar diferente, ouvir diferente, sentir o cheiro diferente, tocar \\ndiferente, comer diferente, assim como os valores sentimentais e \\no aspecto m onetário também são diferentes. Tudo isso é \\nobservado de modos diferentes e tem benefícios e malefícios com \\nvalor de importância para si próprio.   \\nVou tentar imaginar como seria o início de tudo, até \\nporque essa pergunta só gerou guerra, a mesma guerra qu e \\nmoldou a evolução de se adaptar ao próprio movimento inicial. \\nEsse movimento gerou um deslocamento de massa física, pois \\nsem físico não há energia e sem energia não há físico. Quando \\nnossas mães ficam grávidas, logo começamos a precisar do físico \\npara so breviver, nossos neurônios só começam a ser gerados após",
      "position": 126803,
      "chapter": 5,
      "page": 118,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.101724137931036,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 29.0,
        "avg_word_length": 5.339080459770115,
        "unique_word_ratio": 0.7241379310344828,
        "avg_paragraph_length": 174.0,
        "punctuation_density": 0.16091954022988506,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "diferentes",
          "diferente",
          "como",
          "físico",
          "líder",
          "nação",
          "logo",
          "temos",
          "tudo",
          "próprio",
          "gerou",
          "guerra",
          "movimento",
          "energia",
          "carta",
          "presidente",
          "vimos",
          "decorrer",
          "livro",
          "vossa"
        ],
        "entities": [
          [
            "Carta",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "vossa excelência",
            "PERSON"
          ],
          [
            "Logo",
            "GPE"
          ],
          [
            "cheiro diferente",
            "PERSON"
          ],
          [
            "onetário também são",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "como seria o início de tudo",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "grávidas",
            "ORG"
          ]
        ],
        "readability_score": 83.89827586206897,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 126,
        "lexical_diversity": 0.7241379310344828
      },
      "preservation_score": 2.217226703070613e-05
    },
    {
      "id": 1,
      "text": "12 semanas, são os mesmos neurônios que só se correlacionam \\nem aproximadamente 80 por cento após o parto. Esse processo \\nindica o primeiro fator característico de que o corpo orienta a \\nmente.  Assim, a vida vai acontecendo até a mente e o corpo \\nentrarem em equilíbrio ou a mente se torna tão   \\n“inteligente” que te transforma em uma pessoa egocêntrica, \\nradical, extremista, que acredita ser a razão de tudo, afastando as \\npessoas. Falta movimentar -se e isso  é algo que o universo não \\nconseguiu e se conseguir atingir o equilíbrio, possivelmente vai \\nocorrer a estagnação. A falta de movimento, que se cria na \\nausência de energia, implica ausência de energia e, com isso, não \\nse tem vida.   \\nO movimento inicial do u niverso foi tão forte que tivemos \\no Big Bang, Deus, Odin, Buda e qualquer outra grande energia de \\ninício existencial, pois todas tiveram um grande pico de energia e \\ntodas necessitaram de um movimento acima da velocidade da luz. \\nEsses movimentos não consegu em ter tecnologia que consiga \\ncomprovar o movimento acima da própria velocidade da luz, que \\ngerou uma grande liberação de energia em forma de ondas, \\nenergia gravitacional, inércia, centrípeta, caos e todas as energias",
      "position": 128078,
      "chapter": 5,
      "page": 119,
      "segment_type": "page",
      "themes": {
        "filosofia": 39.473684210526315,
        "ciencia": 34.21052631578947,
        "tecnologia": 26.31578947368421
      },
      "difficulty": 32.69770279971285,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.428571428571427,
        "avg_word_length": 4.944723618090452,
        "unique_word_ratio": 0.6633165829145728,
        "avg_paragraph_length": 199.0,
        "punctuation_density": 0.1306532663316583,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "movimento",
          "mente",
          "grande",
          "todas",
          "corpo",
          "vida",
          "equilíbrio",
          "falta",
          "isso",
          "ausência",
          "acima",
          "velocidade",
          "semanas",
          "mesmos",
          "neurônios",
          "correlacionam",
          "aproximadamente",
          "cento",
          "após"
        ],
        "entities": [
          [
            "12",
            "CARDINAL"
          ],
          [
            "são os mesmos neurônios",
            "ORG"
          ],
          [
            "correlacionam",
            "GPE"
          ],
          [
            "80",
            "CARDINAL"
          ],
          [
            "primeiro",
            "GPE"
          ],
          [
            "característico de que",
            "ORG"
          ],
          [
            "Assim",
            "ORG"
          ],
          [
            "entrarem",
            "PERSON"
          ],
          [
            "universo não \\nconseguiu",
            "ORG"
          ],
          [
            "se cria",
            "PERSON"
          ]
        ],
        "readability_score": 84.30229720028716,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 132,
        "lexical_diversity": 0.6633165829145728
      },
      "preservation_score": 2.0741798190015406e-05
    },
    {
      "id": 1,
      "text": "físicas e quânticas tentando adaptar -se ao próprio movimento \\ninicial.   \\nApós essa liberação de energia, começamos a gerar caos \\nadaptativo que gerou vida, morte, bom, ruim, felicidade, \\ntristezas e todas as nossas   \\n“necessidades de um viver territorial”. Vejamos os dinossauros, \\nprimeiros habita ntes em grande proporção territorial, eles foram \\ndestruídos por um meteoro em colisão com a terra, será que essa \\nextinção foi devido à adaptação do universo para equilibrar o \\nmovimento inicial ou devido ao caos gerado pela existência de se \\nter vida no próp rio planeta Terra? Eles viveram por, \\naproximadamente, 200 milhões de anos no planeta, nós \\nhabitamos a apenas 200 mil anos e já estamos próximos \\nnovamente de um viver em um extremo semelhante à Idade \\nMédia.   \\nVamos dar um salto evolutivo para entendermos o ponto \\nem que preciso chegar para tentar mostrar e entender o quanto nós \\nsomos origem do movimento inicial do universo.  Esse \\nmovimento que causa um maior valor energético é o mesmo que \\ncausa um maior valor de  adaptação diante do meu próprio",
      "position": 129402,
      "chapter": 6,
      "page": 120,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 30.779824561403508,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 28.5,
        "avg_word_length": 5.099415204678363,
        "unique_word_ratio": 0.7076023391812866,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.09941520467836257,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "inicial",
          "próprio",
          "essa",
          "caos",
          "vida",
          "viver",
          "territorial",
          "eles",
          "terra",
          "devido",
          "adaptação",
          "universo",
          "planeta",
          "anos",
          "causa",
          "maior",
          "valor",
          "físicas",
          "quânticas"
        ],
        "entities": [
          [
            "Após",
            "PERSON"
          ],
          [
            "Vejamos",
            "PERSON"
          ],
          [
            "extinção foi",
            "PERSON"
          ],
          [
            "universo para",
            "PERSON"
          ],
          [
            "existência de se \\n",
            "PERSON"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "nós \\nhabitamos",
            "ORG"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "já estamos",
            "PERSON"
          ]
        ],
        "readability_score": 84.2201754385965,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 121,
        "lexical_diversity": 0.7076023391812866
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "movimento inicial, assim enxergamos que o caos de adaptação é \\nmaior, pois regula outros caos originários devido ao primeiro \\nmovimento ter um maior valor inicial.    \\nNós humanos vivemos em uma adaptação evolutiva \\ndevido a no ssa própria necessidade, a evolução ocorreu não pela \\nnecessidade de ser forte, e sim de nos tornarmos a espécie mais \\nadaptável de todas para viver confortável. Isso ocorreu não pela \\nnecessidade de comer e sobreviver igual aos outros animais, e sim \\npela cap tação de energia, saber que vai morrer, corpo, sentimento, \\nchácara, espírito, alma e todas as formas de sermos miseráveis \\ndescritas no livro.    \\nApós esse pensamento de sermos o que nós somos, vamos \\nao início do sentimento que gerou todos os miseráveis des critos \\nao longo do livro.    \\nAnalogia    \\nMiseráveis miserável – uma filha(o) de um viciado(a) ou de um \\nhumano que não consegue ter mais que a miséria, como seria a \\naceitação pelo conforto visual, pensamentos e tudo que causaria \\num preconceito sobre ele?",
      "position": 130588,
      "chapter": 6,
      "page": 121,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.714814814814815,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 32.4,
        "avg_word_length": 5.049382716049383,
        "unique_word_ratio": 0.691358024691358,
        "avg_paragraph_length": 162.0,
        "punctuation_density": 0.11728395061728394,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "pela",
          "miseráveis",
          "movimento",
          "inicial",
          "caos",
          "adaptação",
          "maior",
          "outros",
          "devido",
          "ocorreu",
          "mais",
          "todas",
          "sentimento",
          "sermos",
          "livro",
          "assim",
          "enxergamos",
          "pois",
          "regula"
        ],
        "entities": [
          [
            "caos de adaptação",
            "ORG"
          ],
          [
            "Nós",
            "ORG"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "aos outros animais",
            "ORG"
          ],
          [
            "espírito",
            "GPE"
          ],
          [
            "formas de sermos",
            "ORG"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "Analogia",
            "GPE"
          ]
        ],
        "readability_score": 82.28518518518518,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 112,
        "lexical_diversity": 0.691358024691358
      },
      "preservation_score": 1.558458158015677e-05
    },
    {
      "id": 1,
      "text": "Vejo que todos nós temos rugas de expressões, elas são \\ngeradas devido à nossa vivência.  Como essas rugas são geradas \\na partir de expressões, logo entendemos que elas são geradas \\ndevido ao nosso próprio pensamento que ocorre devido ao nosso \\npróprio viver. Se nós pensamos na miséria, como conseguiríamos \\nter um rosto confortável, por exemplo, se não conseguirmos \\npensar na felicidade, no amor, na família, na compaixão, na \\nempatia, na comida, na água, na casa, na cama e no conforto \\ndevido a um viver na miséria?     \\nTodos nós julgamos sem saber o trajeto a ser cumprido na \\nvida, esse mesmo caminho tem um início inevitável da própria \\nvida, seja de miseráveis, seja do líder da nação. Não temos como \\njulgar um passado que não vivemos, porém ele nos molda para o \\nque viv emos no presente. No entanto, os miseráveis do presente, \\nmuitas vezes, não se preocupam com o que já viveram, até porque \\n“quem vive de passado é museu”.    \\nContudo, foi o tempo passado que nos fez entender que a \\nPalestina é um Sodoma e Gomorra onde Moisés pode ter aberto o \\nmar vermelho e Jesus, sendo filho de Deus, representa  a forma \\nmais bela de movimentar -se na Palestina. O budismo é a aceitação",
      "position": 131716,
      "chapter": 6,
      "page": 122,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.27014563106796,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 25.75,
        "avg_word_length": 4.650485436893204,
        "unique_word_ratio": 0.6601941747572816,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.15048543689320387,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "devido",
          "geradas",
          "como",
          "passado",
          "todos",
          "temos",
          "rugas",
          "expressões",
          "elas",
          "nosso",
          "próprio",
          "viver",
          "miséria",
          "vida",
          "seja",
          "miseráveis",
          "presente",
          "palestina",
          "vejo",
          "nossa"
        ],
        "entities": [
          [
            "Vejo",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós temos rugas de expressões",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "nós pensamos",
            "ORG"
          ],
          [
            "seja de miseráveis",
            "ORG"
          ],
          [
            "molda",
            "ORG"
          ],
          [
            "já viveram",
            "PERSON"
          ],
          [
            "Contudo",
            "PERSON"
          ],
          [
            "aberto",
            "PERSON"
          ]
        ],
        "readability_score": 85.72985436893204,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 136,
        "lexical_diversity": 0.6601941747572816
      },
      "preservation_score": 2.43179702917422e-05
    },
    {
      "id": 1,
      "text": "da fome, pois Sidarta Gautama quase morreu devido à \\nnecessidade de comer pouco diante de muitos que comiam pou co. \\nFilosofia é viver no luxo, Sócrates ensinou que a melhor forma de \\naprender é através dos diálogos e debates. A matemática é a \\ndisciplina da exatidão, como não existe exatidão para tudo não \\ntivemos um, e sim vários matemáticos com exatidões para algo. \\nAssim, tivemos Marie curie, AlKhwarizmi, Platão, Isaac Newton, \\nTesla e muitos outros estudiosos.    \\nAtravés de todos os direcionamentos, tivemos grandes \\nlíderes caóticos necessários para aquele determinado tempo, \\nassim surgiu Genghis Khan, o primeiro a junt ar várias tribos \\natravés do medo. Alexandre, o Grande, e Marco Aurélio \\nsignificaram a junção da filosofia e da religião. César, por sua vez, \\nfoi simpatizar com os mesmos que viviam em caos miserável, \\nassim como o Hitler também foi, ambos são a abertura do sexto \\nselo (captação de energia de um caos iminente que a Terra irá ter; \\njudaísmo, estrela de Davi foi a forma mais limpa de movimentar -\\nse entre o caos vivido para o tempo que foi captada).   \\nO mesmo selo que a Terra nos mostrou muito antes de \\nacontecer o próprio cataclisma, anteriormente a Idade Média, foi",
      "position": 133024,
      "chapter": 6,
      "page": 123,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.979,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 25.0,
        "avg_word_length": 4.93,
        "unique_word_ratio": 0.72,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.145,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "através",
          "tivemos",
          "assim",
          "caos",
          "muitos",
          "filosofia",
          "forma",
          "exatidão",
          "como",
          "tempo",
          "selo",
          "terra",
          "fome",
          "pois",
          "sidarta",
          "gautama",
          "quase",
          "morreu",
          "devido",
          "necessidade"
        ],
        "entities": [
          [
            "Sidarta Gautama",
            "PERSON"
          ],
          [
            "pouco diante de muitos que comiam pou co.",
            "PERSON"
          ],
          [
            "Filosofia",
            "PERSON"
          ],
          [
            "Sócrates",
            "GPE"
          ],
          [
            "forma de \\naprender",
            "PERSON"
          ],
          [
            "para tudo não \\ntivemos",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "Marie",
            "PERSON"
          ],
          [
            "AlKhwarizmi",
            "ORG"
          ],
          [
            "Platão",
            "ORG"
          ]
        ],
        "readability_score": 86.021,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 144,
        "lexical_diversity": 0.72
      },
      "preservation_score": 2.2887501451051485e-05
    },
    {
      "id": 1,
      "text": "causado por nós mesmos devido à danificação do planeta Terra, \\no que ocasionou a retirada do eixo gravitacional do universo, \\ncriando doenças no corpo da Terra e isso nos fez viver uma \\nsituação conhecida c omo a idade das trevas.  Ela nos mostrou o \\nquanto somos escravos do próprio sistema caótico involuntário, \\nque evidenciou como movimentar -se entre nós e a Terra, com a \\nbíblia, alcorão, vedas, tripitaka e qualquer livro sagrado que possa \\norientar sobre como movimentar -se no caos vivido de acordo com \\na necessidade territorial.   \\nEntão, vossa  excelência, percebemos que nós \\nhumanos somos  falhos  pelas próprias  desavenças passadas que \\nnem vivemos, porém as nossas  dores,  nossos  caos  são  os  \\nnossos impulsionadores de semelhança de um passado não \\nvivido.  Cabe ressaltar que ele nos causa mal -estar, bem -estar, \\ndores, felicidades, proibições, liberdade, são essas sensações que \\nnos fazem evoluir para algo que não imaginávamos que \\npoderíamos, pois elas nos fazem ter a necessidade de adaptação \\nao próprio movimento.   \\nAgora irei tentar te mostrar uma teoria que demonstra que \\na mente humana dá importância a a lgumas ideias diante de sua \\nprópria necessidade humana, pois essa mesma vem junto à",
      "position": 134349,
      "chapter": 6,
      "page": 124,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 39.7609375,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 38.4,
        "avg_word_length": 5.203125,
        "unique_word_ratio": 0.71875,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.11979166666666667,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "terra",
          "necessidade",
          "somos",
          "próprio",
          "como",
          "movimentar",
          "caos",
          "vivido",
          "dores",
          "nossos",
          "fazem",
          "pois",
          "humana",
          "causado",
          "mesmos",
          "devido",
          "danificação",
          "planeta",
          "ocasionou",
          "retirada"
        ],
        "entities": [
          [
            "mesmos devido",
            "PERSON"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "Ela",
            "PERSON"
          ],
          [
            "quanto somos",
            "PERSON"
          ],
          [
            "nós e a Terra",
            "ORG"
          ],
          [
            "qualquer livro",
            "PERSON"
          ],
          [
            "excelência, percebemos que nós \\nhumanos somos",
            "ORG"
          ],
          [
            "nem vivemos",
            "PERSON"
          ],
          [
            "impulsionadores de semelhança de um",
            "ORG"
          ],
          [
            "poderíamos",
            "PERSON"
          ]
        ],
        "readability_score": 79.2390625,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 138,
        "lexical_diversity": 0.71875
      },
      "preservation_score": 2.0327715104552305e-05
    },
    {
      "id": 1,
      "text": "importância de si próprio. Conseguir usar isso como uma forma \\nde todos nós pensarmos sobre os nossos próprios movimentos \\nsignifica a diminuição do caos caótico que, como fo i citado \\nacima, não pode deixar de existir.",
      "position": 135692,
      "chapter": 6,
      "page": 125,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.508333333333333,
      "complexity_metrics": {
        "word_count": 36,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 18.0,
        "avg_word_length": 5.027777777777778,
        "unique_word_ratio": 0.9166666666666666,
        "avg_paragraph_length": 36.0,
        "punctuation_density": 0.1111111111111111,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "importância",
          "próprio",
          "conseguir",
          "usar",
          "isso",
          "forma",
          "todos",
          "pensarmos",
          "nossos",
          "próprios",
          "movimentos",
          "significa",
          "diminuição",
          "caos",
          "caótico",
          "citado",
          "acima",
          "pode",
          "deixar"
        ],
        "entities": [
          [
            "importância de si próprio",
            "PERSON"
          ],
          [
            "nós pensarmos",
            "ORG"
          ],
          [
            "caos caótico que",
            "PERSON"
          ],
          [
            "acima",
            "GPE"
          ]
        ],
        "readability_score": 89.49166666666667,
        "semantic_density": 0,
        "word_count": 36,
        "unique_words": 33,
        "lexical_diversity": 0.9166666666666666
      },
      "preservation_score": 4.517270023233845e-07
    },
    {
      "id": 1,
      "text": "Pensamento do autor   \\n“Quando concluímos uma conquista, somos felizes com \\nela, porém os outros não acham essa felicidade engraçada. No \\nentanto, quando passamos por alguma dor, ela torna -se \\nengraçada.”   \\n“Ser engraçado é ser amigo da dor, ser feliz é ser inimigo \\ndo sorriso engraç ado.”   \\n  Todos nós somos humanos com sentimentos relativos ao que \\nvivemos, então como podemos sobreviver um para com o outro?",
      "position": 136069,
      "chapter": 6,
      "page": 126,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.921153846153846,
      "complexity_metrics": {
        "word_count": 65,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 16.25,
        "avg_word_length": 5.153846153846154,
        "unique_word_ratio": 0.8769230769230769,
        "avg_paragraph_length": 65.0,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 8,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "somos",
          "engraçada",
          "pensamento",
          "autor",
          "concluímos",
          "conquista",
          "felizes",
          "porém",
          "outros",
          "acham",
          "essa",
          "felicidade",
          "entanto",
          "passamos",
          "alguma",
          "torna",
          "engraçado",
          "amigo",
          "feliz"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "outros não acham",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "ela torna",
            "PERSON"
          ],
          [
            "Todos",
            "ORG"
          ]
        ],
        "readability_score": 90.32884615384616,
        "semantic_density": 0,
        "word_count": 65,
        "unique_words": 57,
        "lexical_diversity": 0.8769230769230769
      },
      "preservation_score": 4.517270023233846e-06
    },
    {
      "id": 1,
      "text": "Imagem ilustrativa",
      "position": 136603,
      "chapter": 6,
      "page": 127,
      "segment_type": "page",
      "themes": {},
      "difficulty": 18.55,
      "complexity_metrics": {
        "word_count": 2,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 2.0,
        "avg_word_length": 8.5,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 2.0,
        "punctuation_density": 0.0,
        "line_break_count": 0,
        "formatting_preservation_score": 35.0
      },
      "analysis": {
        "keywords": [
          "imagem",
          "ilustrativa"
        ],
        "entities": [
          [
            "Imagem",
            "GPE"
          ]
        ],
        "readability_score": 96.45,
        "semantic_density": 0,
        "word_count": 2,
        "unique_words": 2,
        "lexical_diversity": 1.0
      },
      "preservation_score": 0.0
    },
    {
      "id": 1,
      "text": "Como vimos em todo este livro, temos que analisar, \\nentender e compreender. Para fazermos isso, prec isamos \\nmensurar o tamanho do nosso sentimento, logo percebemos \\na dificuldade em reconhecer as próprias dificuldades que a \\nvida nos faz viver involuntariamente e para aqueles que não \\ntem medo de reconhecer a si próprio, esse gráfico acima \\nauxilia para enten der o tamanho do nosso sentimento \\nperante o corpo físico e a importância diante da energia \\ncaptada.   \\nAo analisar o gráfico, temos vermelha, \\namarela, verde, azul, preta e branca. Essas cores \\nsão de intensidade da energia captada e o valor \\ncaptado, assim: vamos colocar um humano que \\nvive na procura de encontrar uma religião, \\nnatureza, esoterismo, espiritismo, estudo e tudo \\naquilo que possa vir c ontrolar o seu excesso de \\nsentimentos ou a falta de sentimentos.   \\nExemplos:  \\nVermelho – esta cor está associada ao humano que \\nvive no extremo do sentimento ou vive no extremo \\nda omissão, pois esses aspectos são grandes",
      "position": 136779,
      "chapter": 6,
      "page": 128,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.43018867924528,
      "complexity_metrics": {
        "word_count": 159,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 31.8,
        "avg_word_length": 5.10062893081761,
        "unique_word_ratio": 0.7358490566037735,
        "avg_paragraph_length": 159.0,
        "punctuation_density": 0.13836477987421383,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sentimento",
          "vive",
          "temos",
          "analisar",
          "tamanho",
          "nosso",
          "reconhecer",
          "gráfico",
          "energia",
          "captada",
          "humano",
          "sentimentos",
          "extremo",
          "como",
          "vimos",
          "todo",
          "este",
          "livro",
          "entender",
          "compreender"
        ],
        "entities": [
          [
            "prec isamos \\nmensurar",
            "PERSON"
          ],
          [
            "logo percebemos",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "medo de reconhecer",
            "PERSON"
          ],
          [
            "acima \\nauxilia",
            "PERSON"
          ],
          [
            "der o",
            "ORG"
          ],
          [
            "corpo físico",
            "PERSON"
          ],
          [
            "temos vermelha",
            "PERSON"
          ],
          [
            "procura de encontrar uma religião",
            "ORG"
          ],
          [
            "que possa vir",
            "PERSON"
          ]
        ],
        "readability_score": 82.56981132075472,
        "semantic_density": 0,
        "word_count": 159,
        "unique_words": 117,
        "lexical_diversity": 0.7358490566037735
      },
      "preservation_score": 1.65633234185241e-05
    },
    {
      "id": 1,
      "text": "captadores de energia. Logo, são mui to intensos \\npara captar a energia, a forma de absorver essa \\nenergia o faz ser muito agressivo quando é \\nnecessário limitar os outros ou o faz absorver o \\nexcesso. Assim, esse sujeito se transforma em um \\nhumano que não consegue direcionar a energia. \\nEssas pes soas têm tem grande risco de ser \\nagressivas, psicopatas, matadoras, de terem \\ndepressão aguda ou Alzheimer (excesso de energia \\nabsorvida mais energia corpórea haverá \\nnecessidade de ter metabolismo relativo de um \\npara com o outro) e outros excessos para cont er a \\nliberação da própria energia.   \\nEsses sujeitos podem ser pessoas que lideram com \\nmais intensidade, amam com mais intensidade, \\nvivem com mais intensidade. Logo, esses \\nhumanos, quando conseguem controlar a sua \\nabsorção de energia, têm mais chances de vi ver \\numa vida muito feliz ou muito triste.",
      "position": 137890,
      "chapter": 6,
      "page": 129,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.11354916067146,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 23.166666666666668,
        "avg_word_length": 5.100719424460432,
        "unique_word_ratio": 0.6834532374100719,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.1223021582733813,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "mais",
          "muito",
          "intensidade",
          "logo",
          "absorver",
          "quando",
          "outros",
          "excesso",
          "esses",
          "captadores",
          "intensos",
          "captar",
          "forma",
          "essa",
          "agressivo",
          "necessário",
          "limitar",
          "assim",
          "esse"
        ],
        "entities": [
          [
            "Logo",
            "PERSON"
          ],
          [
            "para captar",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "necessário limitar",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Essas",
            "GPE"
          ],
          [
            "risco de ser \\nagressivas",
            "PERSON"
          ],
          [
            "matadoras",
            "ORG"
          ]
        ],
        "readability_score": 86.88645083932853,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 95,
        "lexical_diversity": 0.6834532374100719
      },
      "preservation_score": 1.287421956621646e-05
    },
    {
      "id": 1,
      "text": "Metáfora - buraco negro de pequena ou grande absorção de \\nenergia.   \\nAmarelo – esta cor está associada ao indivíduo que \\nnão vive tanto no extremo em relação à cor \\nvermelha, porém é semelhante na forma de ser \\nexplo sivo. A maior diferença está na quantidade de \\nenergia que ele consegue concentrar para \\ndirecionar o seu movimento para ser feliz ou triste, \\nbom ou ruim, viver ou depressivo.   \\nMetáfora – buraco negro de média absorção.   \\nVerde – esta cor remete a sujeitos que são mais \\ncalmos na forma de agir com os seus sentimentos \\ne em resposta à dor física. Assim, são menos \\nagressivos e mais calmos para agir, mas não \\ndeixam de ser agressivos quando precisam limitar \\nalgo que causa incômodo, porém essa \\nagressividade é menos  explosiva em relação ao \\nsujeito que prefere vermelha e amarela.   \\nMetáfora – buraco negro de média absorção.",
      "position": 138876,
      "chapter": 6,
      "page": 130,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.649250749250747,
      "complexity_metrics": {
        "word_count": 143,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 20.428571428571427,
        "avg_word_length": 4.783216783216783,
        "unique_word_ratio": 0.6433566433566433,
        "avg_paragraph_length": 143.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "metáfora",
          "buraco",
          "negro",
          "absorção",
          "energia",
          "esta",
          "está",
          "relação",
          "vermelha",
          "porém",
          "forma",
          "média",
          "mais",
          "calmos",
          "agir",
          "menos",
          "agressivos",
          "pequena",
          "grande",
          "amarelo"
        ],
        "entities": [
          [
            "Amarelo",
            "PERSON"
          ],
          [
            "cor",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para ser",
            "PERSON"
          ],
          [
            "Metáfora",
            "PERSON"
          ],
          [
            "buraco negro de média absorção",
            "ORG"
          ],
          [
            "Verde",
            "PRODUCT"
          ],
          [
            "cor",
            "ORG"
          ],
          [
            "forma de agir",
            "ORG"
          ],
          [
            "para agir",
            "PERSON"
          ]
        ],
        "readability_score": 88.35074925074925,
        "semantic_density": 0,
        "word_count": 143,
        "unique_words": 92,
        "lexical_diversity": 0.6433566433566433
      },
      "preservation_score": 9.486267048791075e-06
    },
    {
      "id": 1,
      "text": "Azul – esta cor está relacionada a sujeitos que são \\ntão calmos que quando percebem o incômodo são \\nagressivos ou depressivos, mas também são óti mos \\nem ter paciência e tranquilidade para resolver os \\nincômodos.   \\nMetáfora – buraco negro de grande ou pequena quantidade em \\nabsorver energia.   \\nPreto e branco – estas cores estão associadas às \\npessoas neutras, ou seja, são aquelas que nunca \\nquerem se met er em momentos em que “não se  \\ndeve” e, quando percebem que deixaram de se \\nmeter em situações em que deveriam ter limitado a \\nsituação, não sabem resolver a própria questão.   \\nMetáfora – o buraco negro secundário é aquele que \\nnão está no centro da galáxia, e sim está neutro na \\ngaláxia.   \\n   Todas as cores remetem a indivíduos que são bons \\ne ruins, verdadeiros e mentirosos, honestos e \\ndesonestos, gananciosos e minimalistas, que amam e \\nodeiam, agressivos e calmos e todas as",
      "position": 139849,
      "chapter": 6,
      "page": 131,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 31.341610738255035,
      "complexity_metrics": {
        "word_count": 149,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 29.8,
        "avg_word_length": 4.805369127516778,
        "unique_word_ratio": 0.6510067114093959,
        "avg_paragraph_length": 149.0,
        "punctuation_density": 0.10067114093959731,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "está",
          "calmos",
          "quando",
          "percebem",
          "agressivos",
          "resolver",
          "metáfora",
          "buraco",
          "negro",
          "cores",
          "galáxia",
          "todas",
          "azul",
          "esta",
          "relacionada",
          "sujeitos",
          "incômodo",
          "depressivos",
          "também",
          "paciência"
        ],
        "entities": [
          [
            "depressivos",
            "GPE"
          ],
          [
            "mas também são óti mos \\nem",
            "PERSON"
          ],
          [
            "Metáfora",
            "PERSON"
          ],
          [
            "buraco negro de",
            "ORG"
          ],
          [
            "estão associadas",
            "PERSON"
          ],
          [
            "querem",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "de se \\nmeter",
            "PERSON"
          ],
          [
            "Metáfora",
            "PERSON"
          ],
          [
            "buraco negro secundário",
            "ORG"
          ]
        ],
        "readability_score": 83.65838926174496,
        "semantic_density": 0,
        "word_count": 149,
        "unique_words": 97,
        "lexical_diversity": 0.6510067114093959
      },
      "preservation_score": 1.21589851458711e-05
    },
    {
      "id": 1,
      "text": "personalidades são construídas a partir do que cada \\nsujeito vive e como interpreta a sua própria \\nimportância para ver a intensidade do sentimento, \\nseja material, seja  sentimental. Esses valores são \\ninterpretados de acordo com o direcionamento da \\nnecessidade de ver a própria vida, temos ricos que \\nquerem ficar mais ricos, temos ricos que não querem \\nser tão ricos, temos pobres que querem ser ricos e \\ntemos pobres que só qu erem viver.  \\nIndependentemente de como cada um de nós quer \\nviver, todos nós nos importamos com algo. Veja \\nalgumas reflexões:   \\nQual é o valor de uma pessoa em sua vida?   \\nQual é o valor de uma casa?   \\nQual é o valor da sua vida?   \\nTudo em nossas vidas é fruto da nossa própria \\nimportância, que nos demostra a nossa \\nnecessidade, seja ela uma comida, seja ela uma \\nbebida, desde água, espinafre, nozes e qualquer \\ncoisa que os nossos corpos pedem como",
      "position": 140861,
      "chapter": 6,
      "page": 132,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.933396404919584,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 21.571428571428573,
        "avg_word_length": 4.708609271523179,
        "unique_word_ratio": 0.5894039735099338,
        "avg_paragraph_length": 151.0,
        "punctuation_density": 0.12582781456953643,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ricos",
          "seja",
          "temos",
          "como",
          "própria",
          "vida",
          "querem",
          "qual",
          "valor",
          "cada",
          "importância",
          "necessidade",
          "pobres",
          "viver",
          "nossa",
          "personalidades",
          "construídas",
          "partir",
          "sujeito",
          "vive"
        ],
        "entities": [
          [
            "construídas",
            "PRODUCT"
          ],
          [
            "querem ficar mais ricos",
            "PERSON"
          ],
          [
            "temos ricos",
            "ORG"
          ],
          [
            "querem \\nser tão ricos",
            "PERSON"
          ],
          [
            "que querem ser",
            "PERSON"
          ],
          [
            "Independentemente de como cada",
            "PERSON"
          ],
          [
            "de nós",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "valor de uma pessoa em sua vida",
            "ORG"
          ],
          [
            "valor de uma casa",
            "ORG"
          ]
        ],
        "readability_score": 87.80170293282876,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 89,
        "lexical_diversity": 0.5894039735099338
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "necessidade fisiológica para algo que “ os nossos \\ncorpos sentem ausência constantemente”. As \\nnossas mentes têm muitas necessidades que não \\nentendemos, esse é o motivo de termos desde uma \\ncor preferida “aquela cor que é a nossa cara” ou até \\nmesmo uma lembrança de felicidade ou tristeza. É \\nimporta nte refletir sobre o valor dos nossos \\nsentimentos diante dos outros, sobre o valor \\nmaterial da sua própria vida e sobre o valor dessas \\npartes da sua vida. Assim, isso nos faz perceber \\nqual é a nossa maior importância em ter o físico e \\no sentimento, sem dei xar de analisar que aquelas \\ncoisas que nós mais nos importamos são as que \\nmais temos sentimentos pela nossa própria vida, \\nseja ela uma pessoa, seja ela uma casa.   \\nPortanto, aqui neste livro eu quero construir, por \\nmeio da escrita, o meu melhor para o plan eta, \\nporém o meu querer nem sempre será válido, \\nprincipalmente quando eu olho o tamanho do meu \\nquerer. Assim, eu chego à conclusão de que eu \\ntentei fazer o meu melhor para o senhor, líder",
      "position": 141868,
      "chapter": 6,
      "page": 133,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 31.21367041198502,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 29.666666666666668,
        "avg_word_length": 4.601123595505618,
        "unique_word_ratio": 0.6853932584269663,
        "avg_paragraph_length": 178.0,
        "punctuation_density": 0.10112359550561797,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "valor",
          "vida",
          "nossos",
          "sentimentos",
          "própria",
          "assim",
          "mais",
          "seja",
          "melhor",
          "querer",
          "necessidade",
          "fisiológica",
          "algo",
          "corpos",
          "sentem",
          "ausência",
          "constantemente",
          "nossas",
          "mentes"
        ],
        "entities": [
          [
            "ausência constantemente",
            "PERSON"
          ],
          [
            "motivo de termos",
            "PERSON"
          ],
          [
            "cor preferida",
            "ORG"
          ],
          [
            "aquela cor",
            "PERSON"
          ],
          [
            "importa nte",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "perceber",
            "PRODUCT"
          ],
          [
            "xar de analisar",
            "PERSON"
          ],
          [
            "nos importamos são",
            "PERSON"
          ],
          [
            "nossa própria",
            "PERSON"
          ]
        ],
        "readability_score": 83.78632958801498,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 122,
        "lexical_diversity": 0.6853932584269663
      },
      "preservation_score": 1.65633234185241e-05
    },
    {
      "id": 1,
      "text": "mundial, pois fazer o meu melhor para você \\nsignifica fazer o melhor para todos do planeta \\nTerra.",
      "position": 143003,
      "chapter": 6,
      "page": 134,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.911764705882355,
      "complexity_metrics": {
        "word_count": 17,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.705882352941177,
        "unique_word_ratio": 0.7647058823529411,
        "avg_paragraph_length": 17.0,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "melhor",
          "mundial",
          "pois",
          "você",
          "significa",
          "todos",
          "planeta",
          "terra"
        ],
        "entities": [
          [
            "meu melhor",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 90.08823529411765,
        "semantic_density": 0,
        "word_count": 17,
        "unique_words": 13,
        "lexical_diversity": 0.7647058823529411
      },
      "preservation_score": 1.5057566744112816e-07
    },
    {
      "id": 1,
      "text": "Carta do autor   \\n   \\nTodos nós produzimos o que nós precisamos \\nconsumir perante a uma quantidade de recursos \\nterritorial. Dentro desses territórios existem \\npadrões de consumação devido aos recursos \\nterritoriais e adaptações evolutivas terem ocorrido \\ndevido a necessidade de “so brevivência” \\nproporcional a quantidade de pessoas, mão de obra, \\nqualificação, consumação, luxúria, adaptação e \\ntudo que “necessitarmos” sermos nos territórios a \\nqual vivemos. Nós humanos produzimos o que \\nvejamos como necessário termos dentro das \\ncivilizaçõ es, essas que contém costumes \\n“evolutivos” dentro de um sistema criado e gerado \\nde acordo com a necessidade de se ter adaptação, \\nseja ela por uma necessidade caótica ou amorosa.    \\n   \\nEsses sistemas (bolsa de valores), foram criados no intuito \\nde termos controle de calcularmos e organizarmos as",
      "position": 143369,
      "chapter": 6,
      "page": 136,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.85557851239669,
      "complexity_metrics": {
        "word_count": 121,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 30.25,
        "avg_word_length": 5.768595041322314,
        "unique_word_ratio": 0.7355371900826446,
        "avg_paragraph_length": 121.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dentro",
          "necessidade",
          "produzimos",
          "quantidade",
          "recursos",
          "territórios",
          "consumação",
          "devido",
          "adaptação",
          "termos",
          "carta",
          "autor",
          "todos",
          "precisamos",
          "consumir",
          "perante",
          "territorial",
          "desses",
          "existem",
          "padrões"
        ],
        "entities": [
          [
            "Carta",
            "ORG"
          ],
          [
            "Todos nós produzimos o",
            "ORG"
          ],
          [
            "evolutivas terem ocorrido \\ndevido",
            "PERSON"
          ],
          [
            "luxúria, adaptação e \\ntudo que",
            "ORG"
          ],
          [
            "necessário termos dentro",
            "ORG"
          ],
          [
            "amorosa",
            "GPE"
          ]
        ],
        "readability_score": 83.14442148760331,
        "semantic_density": 0,
        "word_count": 121,
        "unique_words": 89,
        "lexical_diversity": 0.7355371900826446
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "nossas necessidades de consumação e controle territorial, \\nsendo que, aqueles que produzem mais, mais benefícios \\nde se ter conforto em um viver t erá, não pela necessidade \\nde ter e sim por merecimento em ter.   \\n   \\nEsses que geraram uma maior quantidade de \\nrecursos, são os mesmos que gerar excessos de \\nrecursos para apenas um grupo familiar ou para um \\npequeno grupo de interesses em comum, assim \\ngeramo s o desbalanceamento do “merecimento” \\nde um viver mais confortável.   \\n   \\nÀqueles que herdaram sem saber o valor da \\nconquista, o conquistar torna -se ganancioso, não \\npela necessidade de sobrevivência e sim por não \\nsaber o valor da fome. Essa fome ao ser \\ninterpretada e julgada por aqueles que nunca \\nviveram os mesmos, não sabem a dor que é a fome, \\nlogo a criação do sistema é o próprio \\ndesbalanceamento da quantidade de recursos que",
      "position": 144361,
      "chapter": 6,
      "page": 137,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.0781914893617,
      "complexity_metrics": {
        "word_count": 141,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 35.25,
        "avg_word_length": 4.843971631205674,
        "unique_word_ratio": 0.6312056737588653,
        "avg_paragraph_length": 141.0,
        "punctuation_density": 0.09219858156028368,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "recursos",
          "fome",
          "aqueles",
          "viver",
          "pela",
          "necessidade",
          "merecimento",
          "quantidade",
          "mesmos",
          "grupo",
          "desbalanceamento",
          "saber",
          "valor",
          "nossas",
          "necessidades",
          "consumação",
          "controle",
          "territorial",
          "sendo"
        ],
        "entities": [
          [
            "nossas necessidades de consumação",
            "PERSON"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "geramo s o",
            "ORG"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "da quantidade de recursos",
            "PERSON"
          ]
        ],
        "readability_score": 80.9218085106383,
        "semantic_density": 0,
        "word_count": 141,
        "unique_words": 89,
        "lexical_diversity": 0.6312056737588653
      },
      "preservation_score": 1.1443750725525743e-05
    },
    {
      "id": 1,
      "text": "cada humano necessita ter para um sobreviver \\nsaudável.   \\n   \\n   Voltemos para aque les herdeiros, até porque, \\nsem eles não teríamos a ganância necessária para \\nproduzirmos uma maior quantidade de recursos, \\npois a sua própria ganância pela luxúria é a mesma \\nque o impulsiona a gerar mais conforto para si \\npróprio, assim geramos um sistema de  ciclos \\nnecessários sermos pela própria necessidade de \\ntermos, essa mesma necessidade é relativa para \\ncada um, lembrando que, a minha necessidade não \\nsei produzir, logo o que eu produzo e o que outros \\nproduzem, torna -se valorizado proporcional a \\nnecessidad e de acordo com a oferta e a demanda.   \\n   \\nDevido a esse crescimento ocorrer, a necessidade \\nde se criar mão de obra especializada, \\nconsequentemente causa a proporção da oferta e \\ndemanda do próprio crescimento, logo aquela",
      "position": 145330,
      "chapter": 6,
      "page": 138,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.55769230769231,
      "complexity_metrics": {
        "word_count": 130,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 43.333333333333336,
        "avg_word_length": 5.1923076923076925,
        "unique_word_ratio": 0.7,
        "avg_paragraph_length": 130.0,
        "punctuation_density": 0.1076923076923077,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "cada",
          "ganância",
          "própria",
          "pela",
          "mesma",
          "próprio",
          "logo",
          "oferta",
          "demanda",
          "crescimento",
          "humano",
          "necessita",
          "sobreviver",
          "saudável",
          "voltemos",
          "aque",
          "herdeiros",
          "porque",
          "eles"
        ],
        "entities": [
          [
            "humano necessita",
            "PERSON"
          ],
          [
            "Voltemos",
            "ORG"
          ],
          [
            "ganância pela",
            "PERSON"
          ],
          [
            "própria necessidade de \\ntermos",
            "PERSON"
          ],
          [
            "essa mesma",
            "ORG"
          ],
          [
            "relativa",
            "ORG"
          ],
          [
            "que eu produzo e o",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "da oferta",
            "PERSON"
          ]
        ],
        "readability_score": 76.77564102564102,
        "semantic_density": 0,
        "word_count": 130,
        "unique_words": 91,
        "lexical_diversity": 0.7
      },
      "preservation_score": 1.0728516305180385e-05
    },
    {
      "id": 1,
      "text": "“ganância  de crescimento” torna -se incômodo. \\nAssim percebemos que criamos costumes de \\nconsumação proporcional ao que é necessário \\nvivermos dentro do meio social que eu me \\nencontro ou eu quero ser e ter.   \\n   \\n“Como gostaríamos de ter reconhecimento?   \\nComo gostaríamos de ter reconhecimento monetário, trabalho \\ne pessoal?    \\nAté qual nível o ter reconhecimento é saudável?    \\nEu quero ter reconhecimento ou ser reconhecido?   \\nTer reconhecimento é uma conquista o ser reconhecido é visual.    \\nA minha forma de ser e ter reconhecimento é \\naquela necessária para viver o melhor com aqueles \\nque eu amo.”   \\n   \\n   Vamos pensar: como a própria falta de percepção de \\nsi próprio é o crescimen to de um benefício com \\nmuitos malefícios, esses ocorrem pelo próprio ego de",
      "position": 146284,
      "chapter": 6,
      "page": 139,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.214565826330535,
      "complexity_metrics": {
        "word_count": 119,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 13.222222222222221,
        "avg_word_length": 5.159663865546219,
        "unique_word_ratio": 0.6722689075630253,
        "avg_paragraph_length": 119.0,
        "punctuation_density": 0.09243697478991597,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "reconhecimento",
          "como",
          "quero",
          "gostaríamos",
          "reconhecido",
          "próprio",
          "ganância",
          "crescimento",
          "torna",
          "incômodo",
          "assim",
          "percebemos",
          "criamos",
          "costumes",
          "consumação",
          "proporcional",
          "necessário",
          "vivermos",
          "dentro",
          "meio"
        ],
        "entities": [
          [
            "ganância  de",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "meio social que eu",
            "PERSON"
          ],
          [
            "eu quero ser e ter",
            "PERSON"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "Até",
            "ORG"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "aquela necessária",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ]
        ],
        "readability_score": 91.84098972922503,
        "semantic_density": 0,
        "word_count": 119,
        "unique_words": 80,
        "lexical_diversity": 0.6722689075630253
      },
      "preservation_score": 1.084144805576123e-05
    },
    {
      "id": 1,
      "text": "não querer enxergar e assumir a própria falha, até \\nporque, quem tem coragem de se impor contra aquele \\nque imaginamos estar certo ou por ter mais poder \\nsocial?   \\n   \\nDevido a esse pa radoxo comportamental, não \\nconseguimos sermos semelhantes a “organização \\nde um formigueiro” ... A balança de um viver feliz \\ne alegre é necessária essa inconstância.    \\n   \\nMas essa balança está desbalanceada devido a \\nnossa própria evolução, até porque, eu q uero que o \\nmeu filho tenha uma vida melhor que a minha, por \\nmais que eu não saiba o que possa fazê -lo feliz, \\nlogo o crescimento de um viver melhor é um viver \\nmais preguiçoso em fazer aquelas coisas que nós \\nenxergamos como desconforto, ocasionando falta \\nda mão de obra qualificada primária.",
      "position": 147178,
      "chapter": 7,
      "page": 140,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.70121951219512,
      "complexity_metrics": {
        "word_count": 123,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 30.75,
        "avg_word_length": 4.837398373983739,
        "unique_word_ratio": 0.7235772357723578,
        "avg_paragraph_length": 123.0,
        "punctuation_density": 0.11382113821138211,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "viver",
          "própria",
          "porque",
          "devido",
          "balança",
          "feliz",
          "essa",
          "melhor",
          "querer",
          "enxergar",
          "assumir",
          "falha",
          "quem",
          "coragem",
          "impor",
          "contra",
          "aquele",
          "imaginamos",
          "certo"
        ],
        "entities": [
          [
            "não querer enxergar e",
            "ORG"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "que imaginamos estar",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "essa inconstância",
            "PERSON"
          ],
          [
            "Mas essa balança",
            "ORG"
          ],
          [
            "eu q uero",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "ocasionando",
            "GPE"
          ]
        ],
        "readability_score": 83.17378048780488,
        "semantic_density": 0,
        "word_count": 123,
        "unique_words": 89,
        "lexical_diversity": 0.7235772357723578
      },
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "id": 1,
      "text": "O não enxergar as nossas falhas ao abrir um \\nempreendimento ou ao prestar serviços, muitos \\nnão percebem que são ruins no que fazem, outros \\nnão assumem a própria falha e tem aqueles que não \\nsabem o quão ruins são, já aq ueles que sabem fazer \\nnão falam por querer mais dinheiro, outros não por \\nnão terem paciência para ensinar, temos aqueles \\nque não sabem ensinar e aqueles que não acharam \\nalguém capaz de aprender.   \\n   \\nComo iremos descobrir o quanto valemos se não \\npercebemos  o nosso valor, esse valor só sabemos \\nquando estamos dispostos a receber críticas, \\nconselhos, direcionamentos, carinho, gratidão, \\nafeto, amor, compreensão, compromisso e \\nconfiança pois sem confiança não geramos \\ncredibilidade, sem esses atrativos, não somos  \\ndignos de sermos indicados para um serviço, \\ntrabalho, para um grupo de amigos, para uma \\nfamília e para àquelas coisas em que a maioria das",
      "position": 148046,
      "chapter": 7,
      "page": 141,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.527464788732395,
      "complexity_metrics": {
        "word_count": 142,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 71.0,
        "avg_word_length": 5.091549295774648,
        "unique_word_ratio": 0.704225352112676,
        "avg_paragraph_length": 142.0,
        "punctuation_density": 0.14084507042253522,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "aqueles",
          "sabem",
          "ruins",
          "outros",
          "ensinar",
          "valor",
          "confiança",
          "enxergar",
          "nossas",
          "falhas",
          "abrir",
          "empreendimento",
          "prestar",
          "serviços",
          "muitos",
          "percebem",
          "fazem",
          "assumem",
          "própria",
          "falha"
        ],
        "entities": [
          [
            "não falam",
            "ORG"
          ],
          [
            "querer mais dinheiro",
            "PERSON"
          ],
          [
            "outros não",
            "PERSON"
          ],
          [
            "não terem paciência para ensinar",
            "PERSON"
          ],
          [
            "quanto valemos se não \\npercebemos  o",
            "PERSON"
          ],
          [
            "quando estamos",
            "PERSON"
          ],
          [
            "dispostos",
            "PERSON"
          ],
          [
            "amor",
            "GPE"
          ],
          [
            "compreensão",
            "ORG"
          ]
        ],
        "readability_score": 62.972535211267605,
        "semantic_density": 0,
        "word_count": 142,
        "unique_words": 100,
        "lexical_diversity": 0.704225352112676
      },
      "preservation_score": 1.430468840690718e-05
    },
    {
      "id": 1,
      "text": "pessoas contam com felicidade e alegria quando \\nlembra dos momentos vividos.   \\n   \\nVejo que o nosso valor é originário de acordo com \\na nossa própria importância para com um todo, \\nlogo, quanto mais pessoas nos vê como exemplo, \\nnormalmente e por justiça de privar sua vida para \\num bem maior, ter um ganho e conforto de vida \\nmais satisfatório  do que àqueles que só precisa se \\nimportar consigo mesmo. Ainda nessa linha de \\nraciocínio, os que são bons ou não sabem o quanto \\nsão bons, logo esses bons ficam cansados de não \\nserem bem remunerados e por muitas vezes \\ndesistam da profissão, outros ficam es tagnados \\ndevido a trabalhar e esquecer da própria vida e \\ntemos aqueles que todos adorariam ter, esse é o que \\nvive satisfatoriamente com aquele estilo de vida a \\nqual ele idealizou e realizou.",
      "position": 149053,
      "chapter": 7,
      "page": 142,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.408029197080296,
      "complexity_metrics": {
        "word_count": 137,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 45.666666666666664,
        "avg_word_length": 4.693430656934306,
        "unique_word_ratio": 0.7007299270072993,
        "avg_paragraph_length": 137.0,
        "punctuation_density": 0.08029197080291971,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "bons",
          "pessoas",
          "própria",
          "logo",
          "quanto",
          "mais",
          "ficam",
          "contam",
          "felicidade",
          "alegria",
          "quando",
          "lembra",
          "momentos",
          "vividos",
          "vejo",
          "nosso",
          "valor",
          "originário",
          "acordo"
        ],
        "entities": [
          [
            "pessoas contam com",
            "ORG"
          ],
          [
            "alegria quando",
            "PERSON"
          ],
          [
            "lembra",
            "PERSON"
          ],
          [
            "Vejo",
            "GPE"
          ],
          [
            "originário de acordo",
            "ORG"
          ],
          [
            "quanto mais",
            "PERSON"
          ],
          [
            "precisa se \\nimportar",
            "PERSON"
          ],
          [
            "Ainda",
            "ORG"
          ],
          [
            "de \\nraciocínio",
            "PERSON"
          ],
          [
            "de não \\nserem",
            "PERSON"
          ]
        ],
        "readability_score": 75.75863746958638,
        "semantic_density": 0,
        "word_count": 137,
        "unique_words": 96,
        "lexical_diversity": 0.7007299270072993
      },
      "preservation_score": 7.039412452872742e-06
    },
    {
      "id": 1,
      "text": "Nós temos que perceber o quanto valemos \\nproporcional a grat idão ao nosso entorno, até \\nporque, quanto mais grato nós somos, mais \\ngratidão iremos proporcionar e para gerar isso, \\nmais recursos são necessários. Para gerar conforto \\nao nosso lado, mais conforto temos que ter para \\nconseguir assimilar uma maior quantidade  de \\nproblemas que iremos ter. Devido a sermos gratos \\ne outros também serem gratos em momentos \\nespecíficos, a quais só nós sabíamos o tamanho da \\ngratidão vívida.",
      "position": 149978,
      "chapter": 7,
      "page": 143,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.391774891774894,
      "complexity_metrics": {
        "word_count": 77,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 25.666666666666668,
        "avg_word_length": 5.194805194805195,
        "unique_word_ratio": 0.7402597402597403,
        "avg_paragraph_length": 77.0,
        "punctuation_density": 0.11688311688311688,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "temos",
          "quanto",
          "nosso",
          "gratidão",
          "iremos",
          "gerar",
          "conforto",
          "gratos",
          "perceber",
          "valemos",
          "proporcional",
          "grat",
          "idão",
          "entorno",
          "porque",
          "grato",
          "somos",
          "proporcionar",
          "isso"
        ],
        "entities": [
          [
            "perceber o",
            "ORG"
          ],
          [
            "quanto valemos",
            "PERSON"
          ],
          [
            "quanto mais grato",
            "PERSON"
          ],
          [
            "nosso lado",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "serem gratos",
            "PERSON"
          ],
          [
            "nós sabíamos o tamanho da \\ngratidão",
            "ORG"
          ]
        ],
        "readability_score": 85.60822510822511,
        "semantic_density": 0,
        "word_count": 77,
        "unique_words": 57,
        "lexical_diversity": 0.7402597402597403
      },
      "preservation_score": 3.3879525174253846e-06
    },
    {
      "id": 1,
      "text": "Carta para o eu autor futuro   \\n   \\nDesde o início, não percebemos o iní cio dos nossos \\nmovimentos, pois o mesmo, eu não tive intenção \\nde nascer e nem conviver porém foi necessário \\nadaptar -se, logo vejo que cada humano que nós \\npossamos conhecer, nos façamos dignos de \\nreconhecer quem é para estar ao nosso lado ou não, \\npois não s ão todos que conseguiram reconhecer os \\nseus próprios erros e acertos, logo desejo a você \\nconseguir realizar o seu sonho de comprar um sítio \\npara viver com aqueles que nós confiamos, \\namamos e viver longe da ganância, luxúria, carros \\n(meio de transporte nece ssário para se locomover), \\nonde é necessário aparentarmos sermos \\nsemelhantes aqueles a s quais precisamos viver \\npara conseguirmos “vivermos melhor”, diante de \\nnós “mermos” pensarmos que é necessário em \\nsermos feliz, ter mais conforto, mais dinheiro, mais \\nfama e tudo aquilo que imaginávamos sermos",
      "position": 150600,
      "chapter": 7,
      "page": 144,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.493877551020404,
      "complexity_metrics": {
        "word_count": 147,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 147.0,
        "avg_word_length": 4.979591836734694,
        "unique_word_ratio": 0.7210884353741497,
        "avg_paragraph_length": 147.0,
        "punctuation_density": 0.10204081632653061,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessário",
          "viver",
          "sermos",
          "mais",
          "pois",
          "logo",
          "reconhecer",
          "aqueles",
          "carta",
          "autor",
          "futuro",
          "desde",
          "início",
          "percebemos",
          "nossos",
          "movimentos",
          "mesmo",
          "tive",
          "intenção",
          "nascer"
        ],
        "entities": [
          [
            "Carta",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Desde",
            "ORG"
          ],
          [
            "não percebemos",
            "ORG"
          ],
          [
            "iní cio",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "intenção \\nde nascer e nem",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "vejo",
            "GPE"
          ]
        ],
        "readability_score": 25.006122448979596,
        "semantic_density": 0,
        "word_count": 147,
        "unique_words": 106,
        "lexical_diversity": 0.7210884353741497
      },
      "preservation_score": 1.5735157247597895e-05
    },
    {
      "id": 1,
      "text": "felizes com aquilo, porém não são todos que \\nadquirem aquilo que imaginávamos ser melhor e \\nquando adquirem perdem a felicidade da \\nconfiança, conquista, medo e tudo aquilo que vem \\njunto a admiração alheia do que não pr ovém de \\nsuas próprias conquistas.    \\n   \\nAo pensarmos sobre viver o presente não \\npercebemos o próprio presente, pois o próprio \\npresente veio derivado de um passado necessário \\ndiante do que nós mesmos vivemos, logo percebo \\nque a diferença da evolução humana e a expansão \\ndo universo é a mesma, pois uma têm mais força \\nque a outra, logo vejo se uma não for melhor em \\nadaptar -se a outra a de menor força irá sucumbir.    \\n   \\n“O início do movimento não importa para o \\nsurgimento de uma vida, porém serve para o início \\nde uma evolução.”",
      "position": 151642,
      "chapter": 7,
      "page": 145,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.88549618320611,
      "complexity_metrics": {
        "word_count": 131,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 32.75,
        "avg_word_length": 4.6183206106870225,
        "unique_word_ratio": 0.6564885496183206,
        "avg_paragraph_length": 131.0,
        "punctuation_density": 0.08396946564885496,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "aquilo",
          "presente",
          "porém",
          "adquirem",
          "melhor",
          "próprio",
          "pois",
          "logo",
          "evolução",
          "força",
          "outra",
          "início",
          "felizes",
          "todos",
          "imaginávamos",
          "quando",
          "perdem",
          "felicidade",
          "confiança",
          "conquista"
        ],
        "entities": [
          [
            "que imaginávamos ser melhor e \\nquando",
            "PERSON"
          ],
          [
            "adquirem perdem",
            "ORG"
          ],
          [
            "medo",
            "GPE"
          ],
          [
            "que vem \\njunto",
            "PERSON"
          ],
          [
            "não \\npercebemos o",
            "ORG"
          ],
          [
            "veio derivado de",
            "PERSON"
          ],
          [
            "mesmos vivemos",
            "PERSON"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "importa",
            "NORP"
          ]
        ],
        "readability_score": 82.2395038167939,
        "semantic_density": 0,
        "word_count": 131,
        "unique_words": 86,
        "lexical_diversity": 0.6564885496183206
      },
      "preservation_score": 9.486267048791075e-06
    },
    {
      "id": 1,
      "text": "Nossas brigas entre deuses (religiões), druidas, \\nfilosofia, física, evolução, matemática e tudo \\naquilo que nos fizeram sermos o que nós somos , \\naté chegarmos aonde deveríamos estarmos, para \\nsabermos o que precisávamos sermos e termos um \\nviver melhor... Porém nessa necessidade de se criar \\nregras, leis para conter os próprios erros nos \\nfizeram sermos escravos daqueles que não \\nconseguem viver por m edo em um querer viver \\nmelhor no conforto e luxo, esse mesmo estilo de \\nvida que é exemplo para os miseráveis, torna -se a \\nganância para aqueles que não conseguem chegar \\natravés da inteligência ou sabedoria, até porque de \\nnada tiveram culpa de ter esse racio cínio ruim para \\nsi próprio fazendo a outros sofrerem, e isso, torna -\\nse normal dentro de uma evolução caótica que é \\nnecessário vivermos para não ficarmos estagnados, \\npois se ficarmos estagnados é a ausência de \\nenergia, essa mesma causa a nossa própria falta  de \\nfelicidade, alegria, dor, amor, prazer, satisfação,",
      "position": 152526,
      "chapter": 7,
      "page": 146,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.532075471698114,
      "complexity_metrics": {
        "word_count": 159,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 79.5,
        "avg_word_length": 5.1069182389937104,
        "unique_word_ratio": 0.7295597484276729,
        "avg_paragraph_length": 159.0,
        "punctuation_density": 0.1509433962264151,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sermos",
          "viver",
          "evolução",
          "fizeram",
          "melhor",
          "conseguem",
          "esse",
          "torna",
          "ficarmos",
          "estagnados",
          "nossas",
          "brigas",
          "entre",
          "deuses",
          "religiões",
          "druidas",
          "filosofia",
          "física",
          "matemática",
          "tudo"
        ],
        "entities": [
          [
            "Nossas",
            "GPE"
          ],
          [
            "matemática e tudo \\n",
            "PERSON"
          ],
          [
            "fizeram sermos",
            "ORG"
          ],
          [
            "deveríamos estarmos",
            "PERSON"
          ],
          [
            "precisávamos sermos",
            "PERSON"
          ],
          [
            "leis",
            "PERSON"
          ],
          [
            "fizeram sermos",
            "ORG"
          ],
          [
            "edo",
            "PERSON"
          ],
          [
            "para os miseráveis",
            "PERSON"
          ],
          [
            "ganância para aqueles",
            "PERSON"
          ]
        ],
        "readability_score": 58.717924528301886,
        "semantic_density": 0,
        "word_count": 159,
        "unique_words": 116,
        "lexical_diversity": 0.7295597484276729
      },
      "preservation_score": 2.002656376967005e-05
    },
    {
      "id": 1,
      "text": "adrenalina e singularidade; essa que iria causar a \\nnossa extinção.    \\n   \\nNão preciso estar no seu lugar para saber o quanto \\nestá escasso de mão de obra humana, pois a \\nmesma, já está acontecendo nesse presente \\nmomento em que estou escrevendo essa carta para \\no meu eu futuro, não deixe se abater com as suas \\nepifanias e os seus sur tos existenciais, pois através \\ndeles que você enxerga pensamentos de incômodo \\npara o mundo em um pensamento evolutivo para \\nvocê, pois esse mesmo pensamento que o faz ficar \\nsem saber respostas, são os mesmos que o faz \\nquerer ter respostas. Curta cada aprend izado, cada \\nmomento, cada sentimento e se por acaso você \\nconseguir voltar a sentir prazer no sexo, comida e \\nqualquer outras coisas que não seja uma fuga para \\nsua histeria, usa o fator adrenalina para suprir a \\nnecessidade de recarregar a sua própria energia , até \\nporque é necessário nos movimentarmos para",
      "position": 153636,
      "chapter": 7,
      "page": 147,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.42792207792208,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 51.333333333333336,
        "avg_word_length": 4.759740259740259,
        "unique_word_ratio": 0.7207792207792207,
        "avg_paragraph_length": 154.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "você",
          "cada",
          "adrenalina",
          "essa",
          "saber",
          "está",
          "momento",
          "pensamento",
          "respostas",
          "singularidade",
          "iria",
          "causar",
          "nossa",
          "extinção",
          "preciso",
          "lugar",
          "quanto",
          "escasso",
          "obra"
        ],
        "entities": [
          [
            "adrenalina",
            "GPE"
          ],
          [
            "essa que",
            "ORG"
          ],
          [
            "estar",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para saber",
            "PERSON"
          ],
          [
            "escrevendo essa carta",
            "ORG"
          ],
          [
            "meu eu futuro",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "são os mesmos que",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 72.90541125541125,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 111,
        "lexical_diversity": 0.7207792207792207
      },
      "preservation_score": 1.0013281884835026e-05
    },
    {
      "id": 1,
      "text": "cairmos e levantarmos, amar e odiar, brincar e \\nbrigar, conversar e gritar, debater e xingar, sexo e \\namor, trabalhar e descansar, produzir e curtir, \\napreciar e ignorar, limitar e aproximar de tudo \\naquilo que é necessário fazermos para sermos \\nfelizes. Dentro desse contexto de vida, devemos \\nsermos felizes e engraçados ao mesmo tempo, pois \\nnem todos aqueles que são felizes conseguem \\ncompreender a alegria de um viver do outro por \\nnão ter opção de viver feliz, e si m, ter momentos \\nde felicidade em fazer sexo, beber bebidas baratas, \\ndrogas baratas e tudo aquilo necessário de se ter \\ncomo fuga da sua própria histeria em ter fome, falta \\nde qualidade de vida, estrutura familiar, cama, casa \\ne muitas outras coisas derivadas  de uma adaptação \\ndo movimento inicial da espécie humana.   \\n   \\nNós não somos um humano infeliz, nós \\nprovavelmente vivemos uma vida digna que \\npodemos dizer como foi o trajeto, até porque, nós",
      "position": 154664,
      "chapter": 7,
      "page": 148,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.488157894736844,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 50.666666666666664,
        "avg_word_length": 4.9605263157894735,
        "unique_word_ratio": 0.7302631578947368,
        "avg_paragraph_length": 152.0,
        "punctuation_density": 0.15789473684210525,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "felizes",
          "vida",
          "sexo",
          "tudo",
          "aquilo",
          "necessário",
          "sermos",
          "viver",
          "baratas",
          "como",
          "cairmos",
          "levantarmos",
          "amar",
          "odiar",
          "brincar",
          "brigar",
          "conversar",
          "gritar",
          "debater",
          "xingar"
        ],
        "entities": [
          [
            "cairmos",
            "PERSON"
          ],
          [
            "amar",
            "PERSON"
          ],
          [
            "limitar e aproximar de tudo \\naquilo",
            "ORG"
          ],
          [
            "necessário fazermos",
            "PERSON"
          ],
          [
            "para sermos",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "necessário de se",
            "PERSON"
          ],
          [
            "própria histeria",
            "PERSON"
          ],
          [
            "casa \\ne muitas",
            "ORG"
          ],
          [
            "coisas derivadas  de uma adaptação",
            "PERSON"
          ]
        ],
        "readability_score": 73.17850877192983,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 111,
        "lexical_diversity": 0.7302631578947368
      },
      "preservation_score": 1.7165626088288614e-05
    },
    {
      "id": 1,
      "text": "abrimos os nossos maiores sorrisos quando \\ntropeçamos, quando caím os de cara no chão, \\nquando dormimos e acordamos com uma mulher \\nque não lembro o nome, e quando tivemos \\nqualquer dor ou problema prejudicial ao momento, \\nlogo esse momento é digno de ter um sorriso \\nengraçado não feliz, se esse mesmo for de exemplo \\nem um vive r melhor para alguém ou para algum \\nmomento de nossas vidas, aqui irei começar do \\n“início” da junção dos meus avós.    \\n   \\nUns vieram de uma origem europeia, “bem \\neuropeia” com brasão, muitas terras e muito \\ntradicional devido a escala de distância parentesco , \\nesses que através do sobrenome Jubilado os mais \\ndistantes são primos de primeiro grau, logo \\npercebemos que essa parte hereditária veio com \\num viver caótico do luxo europeu, nesse mesmo \\nlado hereditário veio minha avó de origem \\nindígena, essa mesma que mo rreu muito nova",
      "position": 155711,
      "chapter": 7,
      "page": 149,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.452413793103446,
      "complexity_metrics": {
        "word_count": 145,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 72.5,
        "avg_word_length": 4.841379310344828,
        "unique_word_ratio": 0.7586206896551724,
        "avg_paragraph_length": 145.0,
        "punctuation_density": 0.0896551724137931,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "momento",
          "logo",
          "esse",
          "mesmo",
          "origem",
          "europeia",
          "muito",
          "essa",
          "veio",
          "abrimos",
          "nossos",
          "maiores",
          "sorrisos",
          "tropeçamos",
          "caím",
          "cara",
          "chão",
          "dormimos",
          "acordamos"
        ],
        "entities": [
          [
            "abrimos",
            "PERSON"
          ],
          [
            "sorrisos quando \\ntropeçamos",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "quando dormimos",
            "PERSON"
          ],
          [
            "quando tivemos \\nqualquer",
            "PERSON"
          ],
          [
            "para algum",
            "PERSON"
          ],
          [
            "momento de nossas vidas",
            "ORG"
          ],
          [
            "muito \\ntradicional",
            "PERSON"
          ],
          [
            "Jubilado",
            "PERSON"
          ],
          [
            "primos de primeiro grau",
            "ORG"
          ]
        ],
        "readability_score": 62.297586206896554,
        "semantic_density": 0,
        "word_count": 145,
        "unique_words": 110,
        "lexical_diversity": 0.7586206896551724
      },
      "preservation_score": 1.21589851458711e-05
    },
    {
      "id": 1,
      "text": "deixando seus 5 filhos sem cuidados e um “pai” \\nracista sem compromisso com os próprios \\nmovimentos, deixando todos os movimentos sem \\ndireção a ser seguida, assim minha mãe e meus tios \\ncriaram necessidade de adaptar -se ao próprio \\nmovimento in icial sem culpa de ter nascido.   \\n   \\nA parte do meu pai eu não tenho tantas \\ninformações genealógicas pois o mesmo se \\nausentou durante um bom período de minha vida, \\nmas os meus irmãos viveram mais tempo com ele \\nassim eu fiquei sabendo mais da vida do meu pa i \\natravés dos meus irmãos. Não irei me aprofundar \\nem detalhes prejudiciais a minha própria vida e \\ndaqueles que amo, pois toda a nossa vida e as \\nnossas maiores conquistas são juntos àquelas \\npessoas a qual podemos confiar, amar, brincar, \\nconversar, divertir,  sorrir, gargalhar e tudo aquilo \\nque é demorado de se ter em uma vida com pessoas",
      "position": 156699,
      "chapter": 7,
      "page": 150,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 36.40958904109589,
      "complexity_metrics": {
        "word_count": 146,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 48.666666666666664,
        "avg_word_length": 4.698630136986301,
        "unique_word_ratio": 0.7465753424657534,
        "avg_paragraph_length": 146.0,
        "punctuation_density": 0.0821917808219178,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "minha",
          "meus",
          "deixando",
          "movimentos",
          "assim",
          "pois",
          "irmãos",
          "mais",
          "pessoas",
          "seus",
          "filhos",
          "cuidados",
          "racista",
          "compromisso",
          "próprios",
          "todos",
          "direção",
          "seguida",
          "tios"
        ],
        "entities": [
          [
            "deixando seus",
            "PERSON"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "criaram necessidade de adaptar -se",
            "PERSON"
          ],
          [
            "pai eu",
            "PERSON"
          ],
          [
            "assim eu",
            "PERSON"
          ]
        ],
        "readability_score": 74.25707762557077,
        "semantic_density": 0,
        "word_count": 146,
        "unique_words": 109,
        "lexical_diversity": 0.7465753424657534
      },
      "preservation_score": 1.0163857552276153e-05
    },
    {
      "id": 1,
      "text": "que podemos sentir confiança e amor por termos \\nao nosso lado.    \\n   \\nMeu pai era negão e trabalhava em um meio social \\nde muita ganância, drogas e luxúria necessária para \\nse te r uma vida proporcional ao meio em que os \\nartistas, escola de samba, produtores, \\norganizadores, idealizadores, pensadores e todos \\naqueles que lutam para ter uma vida em liberdade, \\naceitação, compreensão e tudo aquilo que nós \\nenxergamos como certo diante do  nosso próprio \\npensamento em um viver melhor, até porque, \\nseguir um padrão ou um sistema não condiz com o \\nnosso ser feliz, logo entendemos que fazer o \\nnecessário diante de uma necessidade de vida por \\nmuitas vezes ocorrem erros, e isso, é devido à falta \\nde enxergar as falhas do próprio trajeto em um \\nquerer viver melhor com todos aqueles que nós \\n“amamos”.",
      "position": 157672,
      "chapter": 7,
      "page": 151,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.448507462686564,
      "complexity_metrics": {
        "word_count": 134,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 67.0,
        "avg_word_length": 4.8283582089552235,
        "unique_word_ratio": 0.6940298507462687,
        "avg_paragraph_length": 134.0,
        "punctuation_density": 0.11194029850746269,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "vida",
          "meio",
          "todos",
          "aqueles",
          "diante",
          "próprio",
          "viver",
          "melhor",
          "podemos",
          "sentir",
          "confiança",
          "amor",
          "termos",
          "lado",
          "negão",
          "trabalhava",
          "social",
          "muita",
          "ganância"
        ],
        "entities": [
          [
            "que podemos",
            "ORG"
          ],
          [
            "Meu",
            "ORG"
          ],
          [
            "drogas e luxúria necessária",
            "ORG"
          ],
          [
            "para \\nse",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "fazer",
            "ORG"
          ],
          [
            "necessário diante de uma",
            "PERSON"
          ],
          [
            "falta \\nde enxergar",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 65.05149253731344,
        "semantic_density": 0,
        "word_count": 134,
        "unique_words": 93,
        "lexical_diversity": 0.6940298507462687
      },
      "preservation_score": 1.1519038559246305e-05
    },
    {
      "id": 1,
      "text": "Meu pai (negro) e minha mãe (branca) tiveram 4 \\nfilhos negros, o primeiro nasceu em 78, segundo \\n81, terceiro 82 e eu 86, esses 8 anos de diferença \\ndê um para com o outro, provocou \\ninvoluntariamente uma diferença de \\ncomportamento devido a ser gerações difere ntes e \\nqualidade de vida diferente, pois a mesma, tanto o \\nmeu pai quanto minha mãe trabalhavam e tinham \\numa qualidade de vida acima do normal, e essa \\nconquista os fizeram ter uma vida social intensa e \\nnecessária para conseguir fazer network no meio \\nem que viviam e, isso era necessário para conseguir \\nfazer dinheiro proporcional com a qualidade de \\nvida conquistada, ambos vindo de uma origem \\nmiserável com uma inteligência, sabedoria e \\nsagacidade acima da média. Assim nós fomos \\ncriados com muita luxúria e cultu ra, essa, que \\natravés dos artistas (escola de samba, gays, \\nmulheres, preto, branco, gordo, magro, inteligente, \\nburro, egocêntrico) e dos direcionamentos de \\nminha mãe e meu pai nos fizeram sermos humanos",
      "position": 158600,
      "chapter": 7,
      "page": 152,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.50185185185185,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 81.0,
        "avg_word_length": 5.006172839506172,
        "unique_word_ratio": 0.6975308641975309,
        "avg_paragraph_length": 162.0,
        "punctuation_density": 0.1419753086419753,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "minha",
          "qualidade",
          "diferença",
          "acima",
          "essa",
          "fizeram",
          "conseguir",
          "fazer",
          "negro",
          "branca",
          "tiveram",
          "filhos",
          "negros",
          "primeiro",
          "nasceu",
          "segundo",
          "terceiro",
          "esses",
          "anos"
        ],
        "entities": [
          [
            "Meu",
            "ORG"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "primeiro nasceu",
            "PERSON"
          ],
          [
            "78",
            "CARDINAL"
          ],
          [
            "81",
            "CARDINAL"
          ],
          [
            "8 anos de diferença",
            "QUANTITY"
          ],
          [
            "tanto o \\nmeu pai quanto",
            "ORG"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "conquistada",
            "ORG"
          ]
        ],
        "readability_score": 57.99814814814815,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 113,
        "lexical_diversity": 0.6975308641975309
      },
      "preservation_score": 2.1833471778963585e-05
    },
    {
      "id": 1,
      "text": "com um direcionamento fora do padrão, assim ao \\ndecorr er dos anos, cada irmão teve uma forma de \\nser criado ocasionado devido a diferença de termos \\nnascidos com caráter totalmente diferente um do \\noutro, geração diferente uma da outra, porém todos \\ncom um único objetivo de direcionamento em \\nviver o melhor com aq ueles que nós amamos e \\nadmiramos, nos fazendo sermos pessoas que \\nsempre lutamos por algo que vemos como errado e \\npor muitas vezes sendo radicais e extremistas \\ndiante daquele incômodo. Essa criação nos \\nmostrou um direcionamento fora do padrão para \\naqueles h abituados com um sistema de sobreviver \\natravés de regras e sem os seus próprios \\nquestionamentos, os tornando cegos diante de um \\nerro evolutivo pela própria necessidade de ter sido \\ngerado, esse mesmo que nos transforma em seres   \\n“involuídos” por não perceb er os próprios erros, da \\nnossa própria adaptação, em um viver para com o \\noutro.",
      "position": 159709,
      "chapter": 7,
      "page": 153,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.494039735099335,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 75.5,
        "avg_word_length": 4.9801324503311255,
        "unique_word_ratio": 0.695364238410596,
        "avg_paragraph_length": 151.0,
        "punctuation_density": 0.0728476821192053,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "direcionamento",
          "fora",
          "padrão",
          "diferente",
          "outro",
          "viver",
          "diante",
          "próprios",
          "própria",
          "assim",
          "decorr",
          "anos",
          "cada",
          "irmão",
          "teve",
          "forma",
          "criado",
          "ocasionado",
          "devido",
          "diferença"
        ],
        "entities": [
          [
            "decorr",
            "PERSON"
          ],
          [
            "nós amamos",
            "ORG"
          ],
          [
            "fazendo sermos pessoas",
            "ORG"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "para \\naqueles",
            "PERSON"
          ],
          [
            "própria necessidade de ter",
            "ORG"
          ]
        ],
        "readability_score": 60.755960264900665,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 105,
        "lexical_diversity": 0.695364238410596
      },
      "preservation_score": 9.298047464489666e-06
    },
    {
      "id": 1,
      "text": "Quando minha família adquiriu uma qualidade de \\nvida monetária, minha mãe e meu pai chegaram a \\numa conclusão que alguém tinha que deixar de \\ntrabalhar para cuidar melhor dos  seus filhos, como \\nmeu pai tinha mais network e uma maior chance de \\nevoluir no sistema, minha mãe virou dona de casa.    \\n   \\nAo decorrer dos anos meu irmão mais velho por \\nter vivido mais tempo com o meu pai, tornou -se o \\nmais semelhante ao mesmo, os outros d ois irmãos \\ntêm uma diferença de idade de 364 dias, mesmo \\ncom essa  diferença de idade, um nasceu com uma \\ninteligência fora do padrão para o lado da arte \\nsentimental e o outro para o lado da arte material, \\nsendo todos com a sua certeza maior que a certeza \\ndo outro com muitos estudos e determinação em \\nquerer o melhor para a família, gerando conflitos \\ninvoluntários por querer o melhor para o outro \\nsem o outro perceber e por muitas vezes não \\nquerer, sempre acontecendo debates, discussões, \\nconflitos, brigas, dir ecionamentos, conversas e",
      "position": 160755,
      "chapter": 7,
      "page": 154,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 38.3859649122807,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 85.5,
        "avg_word_length": 4.619883040935672,
        "unique_word_ratio": 0.631578947368421,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.0935672514619883,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "outro",
          "minha",
          "melhor",
          "querer",
          "família",
          "tinha",
          "maior",
          "mesmo",
          "diferença",
          "idade",
          "lado",
          "arte",
          "certeza",
          "conflitos",
          "quando",
          "adquiriu",
          "qualidade",
          "vida",
          "monetária"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "vida monetária",
            "PERSON"
          ],
          [
            "trabalhar",
            "NORP"
          ],
          [
            "para cuidar melhor",
            "PERSON"
          ],
          [
            "dona de casa",
            "ORG"
          ],
          [
            "outros",
            "GPE"
          ],
          [
            "diferença de idade de 364",
            "ORG"
          ],
          [
            "essa  diferença de idade",
            "ORG"
          ],
          [
            "padrão",
            "ORG"
          ],
          [
            "para",
            "PRODUCT"
          ]
        ],
        "readability_score": 55.8640350877193,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 108,
        "lexical_diversity": 0.631578947368421
      },
      "preservation_score": 1.2798931732495895e-05
    },
    {
      "id": 1,
      "text": "tudo aquilo que enxergamos como necessário em \\num “viver melhor para o outro”.   \\n   \\nComo já descrevi a base da minha criação na \\nminha forma de ver, agora irei falar como eu \\nenxergo o trajeto da minha vida, até porque o \\ncapítulo a qual estamos lendo é para o eu autor \\nfuturo, logo esse texto é a necessidade de nunca \\nperder a minha própria essência, pois essa veio \\natravés do meu viver com todos e para todos em \\num viver melhor em coletivo, pois quando eu \\nobservo aqueles que chegaram a uma admiração \\npelo o seu dom artístico, o mesmo se perde quando \\na origem desse dom  veio através do seu próprio \\nviver e, o mudar e evoluir o seu próprio viver é o \\nesquecimento de um sentimento não mais vívido, e \\nperder a minha maior construção que é o meu v iver \\ncom todos aqueles que eu amo, não é digno da \\nminha vida, pois essa mesma demorou pelo menos \\n35 anos para ser construída.",
      "position": 161860,
      "chapter": 7,
      "page": 155,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.96606060606061,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 82.5,
        "avg_word_length": 4.2303030303030305,
        "unique_word_ratio": 0.5878787878787879,
        "avg_paragraph_length": 165.0,
        "punctuation_density": 0.07272727272727272,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "viver",
          "como",
          "pois",
          "todos",
          "melhor",
          "vida",
          "perder",
          "essa",
          "veio",
          "através",
          "quando",
          "aqueles",
          "pelo",
          "próprio",
          "tudo",
          "aquilo",
          "enxergamos",
          "necessário",
          "outro"
        ],
        "entities": [
          [
            "tudo aquilo",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "como eu \\nenxergo",
            "PERSON"
          ],
          [
            "lendo",
            "GPE"
          ],
          [
            "para o eu",
            "PERSON"
          ],
          [
            "essa veio",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "quando eu",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ]
        ],
        "readability_score": 57.480909090909094,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 97,
        "lexical_diversity": 0.5878787878787879
      },
      "preservation_score": 1.0013281884835026e-05
    },
    {
      "id": 1,
      "text": "Ao nascer, meus pais moravam em um condomínio com \\nmuitos prédios e famílias de classe média, dentro desse \\ncondomínio quase nã o continham negros e muito menos \\num  homem negro com uma branca e 4 filhos negros; \\nmeu pai estava nos melhores anos de sua vida \\nfinanceira, assim logo construiu uma casa linda, estilo \\ncolonial um terreno de mil m2 com piscina e árvores \\nfrutíferas, uma famí lia “perfeita” tudo para sermos bem \\nsucedidos e filhos com grandes capacidade de serem \\nhumanos de grandes feitos, porém, “em uma vida onde \\ntudo está bom o ter ruim basta um peido.”   \\n   \\nMeus pais separaram quando eu tinha 6 anos e essa \\nseparação deixou minha mãe solteira, sem \\ntrabalho, em uma mansão, 4 filhos negros \\npequenos e todos inteligentes porém “agressivos” \\ndevido ao meio e a necessidade de serem assim, e \\nisso, foi devido a própria necessidade evolutiva em \\num viver melhor ao local onde nós fomos criados.",
      "position": 162866,
      "chapter": 7,
      "page": 156,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.43032258064516,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 77.5,
        "avg_word_length": 4.767741935483871,
        "unique_word_ratio": 0.7225806451612903,
        "avg_paragraph_length": 155.0,
        "punctuation_density": 0.0967741935483871,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "negros",
          "filhos",
          "meus",
          "pais",
          "condomínio",
          "anos",
          "vida",
          "assim",
          "tudo",
          "grandes",
          "serem",
          "porém",
          "onde",
          "devido",
          "necessidade",
          "nascer",
          "moravam",
          "muitos",
          "prédios",
          "famílias"
        ],
        "entities": [
          [
            "meus pais",
            "PERSON"
          ],
          [
            "de classe média",
            "ORG"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "anos de sua",
            "PERSON"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "linda",
            "PERSON"
          ],
          [
            "piscina",
            "NORP"
          ],
          [
            "tudo para sermos",
            "PERSON"
          ],
          [
            "Meus",
            "PERSON"
          ],
          [
            "separaram quando eu",
            "PERSON"
          ]
        ],
        "readability_score": 59.81967741935484,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 112,
        "lexical_diversity": 0.7225806451612903
      },
      "preservation_score": 1.4229400573186614e-05
    },
    {
      "id": 1,
      "text": "Conforme íamos crescendo, fomos criando \\nvínculos familiares de sempre estarmos juntos em \\nfazer o bem de um para com o outro, e esse \\nsentimento, só veio nos dando forças e união diant e \\nda própria necessidade de sobreviver perante a \\nfome, preconceitos e todos aqueles julgamentos ao \\nolharmos uma situação   \\n“incomum”, assim todas as minhas memórias, \\nviraram lembranças e essas lembranças, \\ntornaramse marca tempo da minha própria vida. \\nDuran te todo esse período, eu percebi o quanto um \\nhumano pode ser maior que imagina ser, pois o \\nmesmo se chama Minha Mãe, essa eu não tenho \\npalavras, nem sentimento que eu possa descrever o \\nquanto ela me ensinou a ser o que sempre sonhei \\nser.    \\n   \\nTodas as vez es que eu imaginei estar triste, ela \\nconsegue me fazer feliz independente da sua \\nprópria dor, pois foi assim ao cumprir o papel de",
      "position": 163904,
      "chapter": 7,
      "page": 157,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.43239436619719,
      "complexity_metrics": {
        "word_count": 142,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 47.333333333333336,
        "avg_word_length": 4.774647887323944,
        "unique_word_ratio": 0.7464788732394366,
        "avg_paragraph_length": 142.0,
        "punctuation_density": 0.1056338028169014,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "própria",
          "sempre",
          "fazer",
          "esse",
          "sentimento",
          "assim",
          "todas",
          "lembranças",
          "minha",
          "quanto",
          "pois",
          "conforme",
          "íamos",
          "crescendo",
          "fomos",
          "criando",
          "vínculos",
          "familiares",
          "estarmos",
          "juntos"
        ],
        "entities": [
          [
            "da minha própria",
            "PERSON"
          ],
          [
            "Duran",
            "GPE"
          ],
          [
            "eu percebi",
            "PERSON"
          ],
          [
            "Minha Mãe",
            "PERSON"
          ],
          [
            "essa eu",
            "PERSON"
          ],
          [
            "nem sentimento",
            "PERSON"
          ],
          [
            "que eu possa",
            "PERSON"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "que eu imaginei estar",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ]
        ],
        "readability_score": 74.90093896713614,
        "semantic_density": 0,
        "word_count": 142,
        "unique_words": 106,
        "lexical_diversity": 0.7464788732394366
      },
      "preservation_score": 1.21589851458711e-05
    },
    {
      "id": 1,
      "text": "pai, foi assim ao cumprir o papel da fome, foi assim \\nao cumprir o papel do preconceito, foi assim em \\nser determinada, foi ass im ao direcionar no caos, \\nfoi assim em direcionar quando estava errado \\nperante a outros, foi assim e é assim até hoje.    \\n   \\n“Eu não senti fome, a fome era muito pequena para \\nser sentida quando se é feliz com aqueles que \\namamos, então o meu trajeto em meio  a fome, foi  \\ntranquilo...”   \\n   \\nAprendi valores perante a uma necessidade de ter \\npessoas ao meu lado, até porque tive muitas \\npessoas, que, pior que elas poderiam ser, foram \\nboas para nos ajudar na fome, isso me mostrou \\nvalores em pessoas que não tinham va lores e falta \\nde valores naqueles que tem valores, para aqueles \\nque só enxergam uma aparência.   \\n “Logo novo eu vivi tantas coisas sendo feliz, sem perceber \\no tamanho da miséria.”",
      "position": 164867,
      "chapter": 7,
      "page": 158,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.15205479452055,
      "complexity_metrics": {
        "word_count": 146,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 29.2,
        "avg_word_length": 4.506849315068493,
        "unique_word_ratio": 0.6575342465753424,
        "avg_paragraph_length": 146.0,
        "punctuation_density": 0.1506849315068493,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "fome",
          "valores",
          "pessoas",
          "cumprir",
          "papel",
          "direcionar",
          "quando",
          "perante",
          "feliz",
          "aqueles",
          "preconceito",
          "determinada",
          "caos",
          "estava",
          "errado",
          "outros",
          "hoje",
          "senti",
          "muito"
        ],
        "entities": [
          [
            "quando estava",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "muito pequena para \\nser sentida",
            "PERSON"
          ],
          [
            "amamos",
            "GPE"
          ],
          [
            "poderiam ser",
            "PERSON"
          ],
          [
            "boas",
            "ORG"
          ],
          [
            "tinham va",
            "ORG"
          ],
          [
            "para aqueles \\n",
            "PERSON"
          ],
          [
            "novo eu",
            "PERSON"
          ],
          [
            "coisas",
            "NORP"
          ]
        ],
        "readability_score": 84.04794520547945,
        "semantic_density": 0,
        "word_count": 146,
        "unique_words": 96,
        "lexical_diversity": 0.6575342465753424
      },
      "preservation_score": 1.8596094928979333e-05
    },
    {
      "id": 1,
      "text": "Após alguns anos meu pai voltou a morar em \\nnossa casa e com ele veio meu irmão mais novo \\npor parte de pai, esse mesmo que nos víamos pouco \\ndevido ao afastamento de meu pai por causa de \\nproblemas financeiros e físico, assim eu imagino \\nque o meu pai não teve  forças com as perdas diante \\ndas suas próprias conquistas, fazendo ele se perder \\nna própria decadência e perder -se em voltar uma \\nvida em que ele errou, porém não sabia como \\nrecuperar o próprio erro grave que tinha cometido.    \\n   \\nMeu irmão mais novo é seme lhante a todos os \\nfilhos de meu pai, eu digo que todos nós somos um \\ntime de futebol, um joga na lateral, outro no gol, \\noutro no ataque e quando alguém erra um passe, \\nperde uma bola, nós brigamos, discutimos, \\nparamos de nos falar, nos afastamos, colocamos n o \\nbanco de reserva, mas quando é necessário ser \\nacionado, o mesmo entra no objetivo do time, que \\né fazer o gol. Assim minha mãe sendo Mãe, nunca \\ndeixou de dar amor e carinho para o meu irmão",
      "position": 165824,
      "chapter": 7,
      "page": 159,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.27582417582418,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 60.666666666666664,
        "avg_word_length": 4.252747252747253,
        "unique_word_ratio": 0.6813186813186813,
        "avg_paragraph_length": 182.0,
        "punctuation_density": 0.10989010989010989,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "irmão",
          "mais",
          "novo",
          "mesmo",
          "assim",
          "perder",
          "todos",
          "time",
          "outro",
          "quando",
          "após",
          "alguns",
          "anos",
          "voltou",
          "morar",
          "nossa",
          "casa",
          "veio",
          "parte",
          "esse"
        ],
        "entities": [
          [
            "Após",
            "PERSON"
          ],
          [
            "financeiros",
            "CARDINAL"
          ],
          [
            "assim eu",
            "PERSON"
          ],
          [
            "perdas diante \\ndas suas",
            "PERSON"
          ],
          [
            "Meu",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós brigamos",
            "GPE"
          ],
          [
            "paramos de",
            "PERSON"
          ]
        ],
        "readability_score": 68.39084249084249,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 124,
        "lexical_diversity": 0.6813186813186813
      },
      "preservation_score": 1.581044508131846e-05
    },
    {
      "id": 1,
      "text": "mais novo e tratá-lo como filho, pois o mesmo, nós \\no tratamos da m esma forma que todos são tratados \\ne amado.          \\n   \\nNa escola eu era horrível, porém sempre tranquilo, \\ncalmo, amigo e bom na matemática em nossa \\nmente, não no papel, esse você sabia o resultado e \\nnão sabia fazer o cálculo, isso te fez enxergar \\npadrões i gual quando copiávamos desenhos de \\nanimais e mangás japonês, esse mesmo padrão \\nadquirido o fez ser um ótimo profissional em \\ninstalar Insulfilm e plotagem em geral, pois ao \\ncortar nós conseguimos assimilar as memórias de \\ncopiar os desenhos em gravar o traça do, e isso, nos \\nfez termos facilidade em trabalhar e se destacar em \\numa profissão que nos deu comida, casa, estrutura \\nfamiliar, bom estudo para o nosso filho, \\nfelicidades, alegrias, prazeres, momentos \\ninesquecíveis e tudo que uma vida digna em fazer \\no que é necessário para um viver melhor para si \\npróprio com todos aqueles que nós amamos.",
      "position": 166924,
      "chapter": 8,
      "page": 160,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.41509433962264,
      "complexity_metrics": {
        "word_count": 159,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 79.5,
        "avg_word_length": 4.716981132075472,
        "unique_word_ratio": 0.7232704402515723,
        "avg_paragraph_length": 159.0,
        "punctuation_density": 0.1320754716981132,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "filho",
          "pois",
          "mesmo",
          "todos",
          "esse",
          "sabia",
          "fazer",
          "isso",
          "desenhos",
          "mais",
          "novo",
          "tratá",
          "como",
          "tratamos",
          "esma",
          "forma",
          "tratados",
          "amado",
          "escola",
          "horrível"
        ],
        "entities": [
          [
            "mais novo",
            "PERSON"
          ],
          [
            "tratá-lo",
            "PERSON"
          ],
          [
            "nós \\no tratamos da m",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "quando copiávamos",
            "PERSON"
          ],
          [
            "desenhos de \\nanimais e mangás japonês",
            "ORG"
          ],
          [
            "adquirido o fez",
            "PERSON"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 58.83490566037736,
        "semantic_density": 0,
        "word_count": 159,
        "unique_words": 115,
        "lexical_diversity": 0.7232704402515723
      },
      "preservation_score": 1.65633234185241e-05
    },
    {
      "id": 1,
      "text": "Desde novo sempre sonhei em ter uma esposa, \\nfilho e aquela coisa de família tradicional que nos \\né colocado na cabeça como um viver melhor, pois \\no nosso viver melhor é diferente daqueles \\npensamentos tradicionais, nós queremos ser \\nconquistados assim como queremos conquistar, o \\nviver um relacionamento onde não podemos \\nsermos nós mesmos, não é digno de ser vívido, \\nnem por você e nem pela a outra pessoa que está \\nao seu lado,  até porque, aqueles que nos amam \\nfizeram sacrifícios para sermos feliz e o não \\naproveitar é uma falta de valor para aqueles que \\nsofreram para você viver, pois assim como nós não \\npercebemos o  \\nmal que causamos a outros, outros também não \\npercebem o mal que  nos causam, e isso não é bom \\npara ninguém. Assim como nós um dia tivemos \\nesse sonho e vivemos esse sonho e não desistimos \\nde vivenciá -lo novamente, hoje nós sabemos o que",
      "position": 167983,
      "chapter": 8,
      "page": 161,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.3796052631579,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 76.0,
        "avg_word_length": 4.598684210526316,
        "unique_word_ratio": 0.618421052631579,
        "avg_paragraph_length": 152.0,
        "punctuation_density": 0.08552631578947369,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "viver",
          "assim",
          "melhor",
          "pois",
          "queremos",
          "sermos",
          "você",
          "aqueles",
          "outros",
          "esse",
          "sonho",
          "desde",
          "novo",
          "sempre",
          "sonhei",
          "esposa",
          "filho",
          "aquela",
          "coisa"
        ],
        "entities": [
          [
            "Desde",
            "ORG"
          ],
          [
            "aquela coisa de família",
            "PERSON"
          ],
          [
            "nós queremos",
            "GPE"
          ],
          [
            "nós mesmos",
            "ORG"
          ],
          [
            "não é digno de ser",
            "ORG"
          ],
          [
            "nem pela",
            "PERSON"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "para sermos",
            "PERSON"
          ],
          [
            "falta de valor",
            "ORG"
          ],
          [
            "sofreram",
            "ORG"
          ]
        ],
        "readability_score": 60.62039473684211,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 94,
        "lexical_diversity": 0.618421052631579
      },
      "preservation_score": 9.486267048791075e-06
    },
    {
      "id": 1,
      "text": "queremos, nos fazendo termos mais sabedoria em \\ncurtir o trajeto da conquista de uma vida em \\ncomum acordo em viver até o final da vida em um \\núnico objetivo de serem felizes.   \\n   \\n“Ao realizar um sonho, esse foi o meu maior pesadelo.”   \\n   \\nQuando se cria muita expectativa em algo, o valor \\ndaquela expectativa gerada é a mesma proporção \\nda depressão adquirida quando se perde esse \\nsonho, assim foi a minha maior depressão mental \\nque eu vivi, pois essa eu já tinha realizado ao ter \\numa esposa, fil ho, familiares e amigos, logo a \\nminha vida com dificuldades ter vivido o melhor \\nque uma vida possa viver, perder isso foi a queda \\nde uma dificuldade em conquistar o meu “maior \\nobjetivo”, esse objetivo, um pouco mais para frente \\nvocê percebeu que o motivo d a vida não era \\nbaseada nos estereótipos criados como o melhor da \\nvida, e sim poderia ser vários melhores, vários",
      "position": 168975,
      "chapter": 8,
      "page": 162,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.37647058823529,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 51.0,
        "avg_word_length": 4.588235294117647,
        "unique_word_ratio": 0.673202614379085,
        "avg_paragraph_length": 153.0,
        "punctuation_density": 0.09803921568627451,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "objetivo",
          "esse",
          "maior",
          "mais",
          "viver",
          "sonho",
          "quando",
          "expectativa",
          "depressão",
          "minha",
          "melhor",
          "vários",
          "queremos",
          "fazendo",
          "termos",
          "sabedoria",
          "curtir",
          "trajeto",
          "conquista"
        ],
        "entities": [
          [
            "fazendo termos mais",
            "ORG"
          ],
          [
            "Quando se",
            "PERSON"
          ],
          [
            "da depressão",
            "ORG"
          ],
          [
            "quando se perde",
            "PERSON"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "essa eu já tinha",
            "PERSON"
          ],
          [
            "pouco mais",
            "PERSON"
          ],
          [
            "para frente \\nvocê percebeu que",
            "PERSON"
          ]
        ],
        "readability_score": 73.12352941176471,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 103,
        "lexical_diversity": 0.673202614379085
      },
      "preservation_score": 1.3589453986561819e-05
    },
    {
      "id": 1,
      "text": "momentos, várias pessoas, várias formas de ser \\nfeliz e essa felicidade você perceberá que não \\ndependia só de nós, e sim de todos aqueles que \\ntrouxeram a energia necessária para cada momento \\nque nós vivenciamos, sejamos gratos por já ter \\nconseguido amar e cada momento de loucuras que \\nvivenciamos, essa nos fizera termos sensações \\nindescritíveis de companheirismo, amizade, \\nconfiança, aconchego, amor , carinho, \\ncompreensão, todos os problemas, falta de \\nconfiança, dores e aquelas coisas necessárias \\nvivermos para sabermos o que nos faz \\nentendermos, o melhor para você.    \\n   \\nEssa depressão vívida, pode se dizer que foi uma \\ndas melhores coisas que poderia ter acontecido, \\nessa que foi a causa do nosso descobrimento em \\nviver em fuga pelo próprio prazeres, simplesmente \\npelo fato de não perceber que o sentimento sentido \\no controlava mais que a sua mente, logo a sua \\nhisteria se engrandeceu com a sua perda, essa",
      "position": 169975,
      "chapter": 8,
      "page": 163,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.56164383561644,
      "complexity_metrics": {
        "word_count": 146,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 73.0,
        "avg_word_length": 5.205479452054795,
        "unique_word_ratio": 0.684931506849315,
        "avg_paragraph_length": 146.0,
        "punctuation_density": 0.14383561643835616,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "essa",
          "várias",
          "você",
          "todos",
          "cada",
          "momento",
          "vivenciamos",
          "confiança",
          "coisas",
          "pelo",
          "momentos",
          "pessoas",
          "formas",
          "feliz",
          "felicidade",
          "perceberá",
          "dependia",
          "aqueles",
          "trouxeram",
          "energia"
        ],
        "entities": [
          [
            "várias formas de ser",
            "PERSON"
          ],
          [
            "essa felicidade você perceberá que",
            "ORG"
          ],
          [
            "para cada",
            "PERSON"
          ],
          [
            "que nós vivenciamos",
            "ORG"
          ],
          [
            "sejamos gratos",
            "GPE"
          ],
          [
            "amar e cada",
            "PERSON"
          ],
          [
            "momento de loucuras que \\nvivenciamos",
            "ORG"
          ],
          [
            "confiança",
            "GPE"
          ],
          [
            "aconchego",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 61.93835616438356,
        "semantic_density": 0,
        "word_count": 146,
        "unique_words": 100,
        "lexical_diversity": 0.684931506849315
      },
      "preservation_score": 1.581044508131846e-05
    },
    {
      "id": 1,
      "text": "histeria que nós vivemos as maiores loucuras, \\nalegrias, tristezas, conhecimentos, superação, \\nadaptação, entendimento e compreensão com \\ntodos aqueles que erramos para aprender a \\nmelhorar o seu próprio viver, assim vejo a nossa \\ngratidão por ter tido todos os  “problemas” \\nnecessários. Nesse aprendizado de interpretar o \\npróprio sentimento, todas as vezes que nós \\natingíamos um pico de histeria, você estudava, \\nconversava, procurava, debatia, perguntava em \\ntodas as crenças filosóficas, religiosas, psicologia, \\nneuro ciência, matemática, física, química, \\nalimentação, física quântica, história, darwinismo \\nquântico, arquétipos platônicos, Fibonacci, Tesla, \\nEinstein e qualquer estudo que pudesse ter uma \\nresposta plausível, até porque, nós aprendemos \\natravés de procurar os  nossos porquês diretamente \\nao Cadê, e hoje, eu procuro no Google todas \\naquelas respostas que eu tinha preguiça em ler um \\nlivro inteiro para adquirir apenas uma frase, \\nlembre -se que nosso cérebro têm uma quantidade",
      "position": 171023,
      "chapter": 8,
      "page": 164,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.82589928057554,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 69.5,
        "avg_word_length": 6.086330935251799,
        "unique_word_ratio": 0.8057553956834532,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.23741007194244604,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todas",
          "histeria",
          "todos",
          "próprio",
          "física",
          "vivemos",
          "maiores",
          "loucuras",
          "alegrias",
          "tristezas",
          "conhecimentos",
          "superação",
          "adaptação",
          "entendimento",
          "compreensão",
          "aqueles",
          "erramos",
          "aprender",
          "melhorar",
          "viver"
        ],
        "entities": [
          [
            "histeria que nós vivemos",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "vejo",
            "GPE"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "pico de histeria",
            "ORG"
          ],
          [
            "debatia",
            "GPE"
          ],
          [
            "religiosas",
            "GPE"
          ],
          [
            "psicologia",
            "GPE"
          ],
          [
            "neuro ciência",
            "PERSON"
          ],
          [
            "matemática",
            "GPE"
          ]
        ],
        "readability_score": 63.42410071942446,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 112,
        "lexical_diversity": 0.8057553956834532
      },
      "preservation_score": 2.7103620139403077e-05
    },
    {
      "id": 1,
      "text": "de processamento limitado, logo vejo a \\nnecessidade de lembrar, que nada adianta pensar \\nem alguma coisa se você não concluiu o que tem \\num maior valor no momento em que é necessário \\nser pensado e feito.   \\n   \\nNunca atropele um sonho que você sonhou, pois \\nesse mesmo a uma semana atrás nos mostrou \\ninconscientemente um problema que me  \\nincomodava e não percebia, esse “problema” só foi \\npercebido por nós, graças aos pesadelos que \\ntínhamos com frequência quando éramos crianças, \\nesses pesadelos que eram devidos aos filmes de \\nterror que passava em um canal d e tv aberta na \\nmadrugada, pois desde novo tínhamos dificuldades \\nem dormir e quando conseguíamos dormir \\ntínhamos pesadelos, esses tiveram que ser \\ncontrolados devido ao medo que nos causava, \\nassim começamos a usar isso a nosso favor para \\nconseguirmos interpr etar e nunca sofrer com \\npesadelos. Quando tínhamos pesadelos nós",
      "position": 172146,
      "chapter": 8,
      "page": 165,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.52517482517483,
      "complexity_metrics": {
        "word_count": 143,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 47.666666666666664,
        "avg_word_length": 5.083916083916084,
        "unique_word_ratio": 0.7202797202797203,
        "avg_paragraph_length": 143.0,
        "punctuation_density": 0.07692307692307693,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pesadelos",
          "tínhamos",
          "quando",
          "você",
          "nunca",
          "pois",
          "esse",
          "problema",
          "esses",
          "dormir",
          "processamento",
          "limitado",
          "logo",
          "vejo",
          "necessidade",
          "lembrar",
          "nada",
          "adianta",
          "pensar",
          "alguma"
        ],
        "entities": [
          [
            "vejo",
            "ORG"
          ],
          [
            "que nada",
            "PERSON"
          ],
          [
            "coisa se você não concluiu",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "ser pensado e feito",
            "ORG"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "sonhou",
            "GPE"
          ],
          [
            "frequência quando éramos",
            "PERSON"
          ],
          [
            "que passava",
            "PERSON"
          ],
          [
            "quando conseguíamos",
            "PERSON"
          ]
        ],
        "readability_score": 74.64149184149184,
        "semantic_density": 0,
        "word_count": 143,
        "unique_words": 103,
        "lexical_diversity": 0.7202797202797203
      },
      "preservation_score": 9.787418383673333e-06
    },
    {
      "id": 1,
      "text": "começamos a criar mecanismo de defesa, por \\nmuitas vezes éramos o Super Homem outras vezes \\no Batman, hoje, você não morre nos seus sonhos, \\nnós ficamos em um loop de repetição do mesmo \\nsonho, e m trajetos diferentes e a forma de \\ninterpretar sendo a mesma, pois esse sonho que \\nestava nos incomodando, você sempre morria \\ndevido a necessidade de estar preso a alguma \\npessoa... Devido ao pensamento ser o mesmo,  fez \\nperceber o quão cansado estou do meu trabalho de \\nInsulfilm, pois esse trabalho que me fez ter o que é \\nnecessário para um viver melhor, é o mesmo que \\nexige muito de nossos corpos para conseguir \\nsobreviver dignamente, e isso, só é necessário \\nmanter devido a ser o nosso sustento e daqueles \\nque p recisam de nós, assim nós percebemos a \\nnecessidade de viver e aceitar, até porque, o que \\nnós estaríamos fazendo de melhor, que trabalhar e \\nganhar o direito de viver a nossa liberdade?",
      "position": 173158,
      "chapter": 8,
      "page": 166,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.38607594936709,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 79.0,
        "avg_word_length": 4.620253164556962,
        "unique_word_ratio": 0.6392405063291139,
        "avg_paragraph_length": 158.0,
        "punctuation_density": 0.12658227848101267,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mesmo",
          "devido",
          "viver",
          "vezes",
          "você",
          "sonho",
          "pois",
          "esse",
          "necessidade",
          "trabalho",
          "necessário",
          "melhor",
          "começamos",
          "criar",
          "mecanismo",
          "defesa",
          "muitas",
          "éramos",
          "super",
          "homem"
        ],
        "entities": [
          [
            "Super Homem",
            "ORG"
          ],
          [
            "Batman",
            "GPE"
          ],
          [
            "necessidade de estar",
            "ORG"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "pensamento ser o mesmo",
            "ORG"
          ],
          [
            "perceber o",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "muito de nossos",
            "PERSON"
          ],
          [
            "sobreviver dignamente",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 59.11392405063291,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 101,
        "lexical_diversity": 0.6392405063291139
      },
      "preservation_score": 1.3551810069701539e-05
    },
    {
      "id": 1,
      "text": "Esse pensamento me gerou uma conclusão que eu \\nvejo como a melhor forma de vivermos, pois o \\nnosso viver futuro só depende de manter tudo \\naquilo que conquistamos, por isso vejo que \\nconstruir um local onde todos aqueles que você \\nconfia e ama, possam curtir e viver como \\ndeveríamos viver, essa é a conclusão do nosso \\nparar de pensar na fome e chegar na forma de vida \\nque será a maior histeria em sermos felizes.   \\n“Não adianta eu fazer o melhor para humanidade \\nse a própria humanidade não está fazendo bem para \\nmim.”    \\nO querer ter fama, ter reconhecimento, ter dinheiro, \\nter sexo, ter “amigos “e querer ter o que não é para \\nter é um dos caminhos propícios a perder o próprio \\nviver.   \\nAté que ponto necessitamos ter ou ser mais, para viver \\nmelhor com aqueles que precisamo s viver?",
      "position": 174187,
      "chapter": 8,
      "page": 167,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.09255319148936,
      "complexity_metrics": {
        "word_count": 141,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 35.25,
        "avg_word_length": 4.475177304964539,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 141.0,
        "punctuation_density": 0.09219858156028368,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "melhor",
          "conclusão",
          "vejo",
          "como",
          "forma",
          "nosso",
          "aqueles",
          "humanidade",
          "querer",
          "esse",
          "pensamento",
          "gerou",
          "vivermos",
          "pois",
          "futuro",
          "depende",
          "manter",
          "tudo",
          "aquilo"
        ],
        "entities": [
          [
            "que eu \\nvejo",
            "PERSON"
          ],
          [
            "melhor forma de vivermos",
            "PERSON"
          ],
          [
            "que conquistamos",
            "PERSON"
          ],
          [
            "vejo que",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "possam curtir",
            "ORG"
          ],
          [
            "para \\nmim",
            "PERSON"
          ]
        ],
        "readability_score": 81.03244680851064,
        "semantic_density": 0,
        "word_count": 141,
        "unique_words": 94,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "id": 1,
      "text": "“Nós temos tantos medos da fome, que os lugares \\nonde se vive na miséria é de se ter medo.” O que é \\nperigoso?    \\nNossos pensamentos são dignos de confiança?   \\nAqui eu deixo um pedido de socorro pela empatia \\npois aqueles que vivem na miséria já est ão \\nacostumados com o medo.   \\nAqueles que vivem na miséria não podem errar.    \\nAqueles que vivem com fome não têm direito de reclamar.   \\nAqueles que têm fome, ficam com a aparência tão \\nmiserável, que viram motivo para ser julgado como \\nbandido.   \\nAqueles que  vivem acima da linha da pobreza tem \\ntanto medo da fome, que o seu conforto de viver é \\nmais importante que a fome dos miseráveis.   \\nTodos nós só queremos enxergar o nosso próprio rabo.   \\nTodos nós só queremos ter e ser para si próprio, um ganancioso \\nproporcional ao luxo miserável.",
      "position": 175100,
      "chapter": 8,
      "page": 168,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.35539568345324,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 13.9,
        "avg_word_length": 4.517985611510792,
        "unique_word_ratio": 0.6618705035971223,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.1079136690647482,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fome",
          "aqueles",
          "vivem",
          "miséria",
          "medo",
          "miserável",
          "todos",
          "queremos",
          "próprio",
          "temos",
          "tantos",
          "medos",
          "lugares",
          "onde",
          "vive",
          "perigoso",
          "nossos",
          "pensamentos",
          "dignos",
          "confiança"
        ],
        "entities": [
          [
            "Nossos",
            "ORG"
          ],
          [
            "Aqui eu",
            "PERSON"
          ],
          [
            "medo",
            "GPE"
          ],
          [
            "Aqueles",
            "PERSON"
          ],
          [
            "Aqueles",
            "PERSON"
          ],
          [
            "têm direito de reclamar",
            "ORG"
          ],
          [
            "julgado como \\nbandido",
            "PERSON"
          ],
          [
            "vivem acima da linha da pobreza",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "miseráveis",
            "DATE"
          ]
        ],
        "readability_score": 91.69460431654676,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 92,
        "lexical_diversity": 0.6618705035971223
      },
      "preservation_score": 1.0879091972621509e-05
    },
    {
      "id": 1,
      "text": "Aqui está o meu apelo em refletir e enxergar que a \\nnossa vida miserável é maior que de muitos outros \\nmiseráveis!!!   \\nEssas são as palavras de um ex miserável!! !",
      "position": 176021,
      "chapter": 8,
      "page": 169,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.55,
      "complexity_metrics": {
        "word_count": 30,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 4.333333333333333,
        "unique_word_ratio": 0.9333333333333333,
        "avg_paragraph_length": 30.0,
        "punctuation_density": 0.2,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "miserável",
          "aqui",
          "está",
          "apelo",
          "refletir",
          "enxergar",
          "nossa",
          "vida",
          "maior",
          "muitos",
          "outros",
          "miseráveis",
          "essas",
          "palavras"
        ],
        "entities": [
          [
            "Essas",
            "GPE"
          ]
        ],
        "readability_score": 91.2,
        "semantic_density": 0,
        "word_count": 30,
        "unique_words": 28,
        "lexical_diversity": 0.9333333333333333
      },
      "preservation_score": 6.775905034850767e-07
    }
  ],
  "book_name": "O_Presidente_diagramado 1.pdf",
  "book_cover": "book_cover.png"
}"""
        
        if not analysis_data_str or analysis_data_str == "##BOOK_ANALYSIS_DATA##":
            st.error("🚨 Dados de análise não encontrados")
            st.info("""
            📋 **Solução de problemas:**
            1. Execute primeiro a análise do livro no módulo principal
            2. Aguarde o processamento completo dos dados
            3. Recarregue a página após a análise ser concluída
            """)
            
            if st.button("📊 Executar Análise do Livro", type="primary"):
                st.switch_page("main_analysis.py")
            return
        
        analysis_data_str = analysis_data_str.strip()
        
        if analysis_data_str.startswith('"""') and analysis_data_str.endswith('"""'):
            analysis_data_str = analysis_data_str[3:-3].strip()
        
        try:
            analysis_data = json.loads(analysis_data_str)
            st.success("✅ JSON carregado com sucesso!")
        except json.JSONDecodeError as e:
            st.error(f"🚨 Erro ao decodificar JSON: {str(e)}")
            
            st.text(f"Linha: {e.lineno}, Coluna: {e.colno}, Char: {e.pos}")
            
            start = max(0, e.pos - 100)
            end = min(len(analysis_data_str), e.pos + 100)
            error_context = analysis_data_str[start:end]
            st.code(f"...{error_context}...", language="json")
            
            try:
                cleaned_json = analysis_data_str
                cleaned_json = re.sub(r'(?<!\\)"', '\\"', cleaned_json)
                cleaned_json = cleaned_json.replace('\n', '\\n').replace('\r', '\\r')
                
                analysis_data = json.loads(f'"{cleaned_json}"')
                st.success("✅ JSON reparado manualmente!")
            except Exception as e2:
                st.error(f"❌ Não foi possível reparar o JSON: {str(e2)}")
                st.info("""
                📋 **Solução de problemas:**
                1. Verifique se os dados de análise estão no formato JSON válido
                2. Execute novamente a análise do livro
                3. Se o problema persistir, verifique o arquivo de origem
                """)
                return
        
        if not analysis_data or 'segments' not in analysis_data:
            st.error("🚨 Estrutura de dados inválida: campo 'segments' não encontrado")
            st.info("""
            📋 **Solução de problemas:**
            1. Verifique se o arquivo de análise foi gerado corretamente
            2. Certifique-se de que o processo de análise foi concluído com sucesso
            3. Execute novamente a análise do livro
            """)
            return
        
        reader = QuantumBookReader(analysis_data)
        reader.render()
        
    except Exception as e:
        st.error(f"🚨 Erro inesperado: {str(e)}")
        st.info("""
        📋 **Solução de problemas:**
        1. Recarregue a página e tente novamente
        2. Verifique se há problemas com seus dados de entrada
        3. Consulte o suporte técnico se o problema persistir
        """)

if __name__ == "__main__":
    main()