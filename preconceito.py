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
    "total_segments": 139,
    "total_chapters": 19,
    "total_pages": 139,
    "avg_difficulty": 33.5889878849788,
    "max_difficulty": 42.577319587628864,
    "min_difficulty": 21.218556701030927,
    "theme_distribution": {
      "ciencia": 63.469193132401934,
      "tecnologia": 31.485074891825462,
      "filosofia": 78.46015940735373,
      "arte": 77.3416179337232
    },
    "total_words": 28494,
    "avg_words_per_segment": 204.9928057553957,
    "formatting_preservation": 80.0,
    "preservation_score": 2.1757706037179813e-05,
    "book_name": "preconceito_Quântico_finalizado_editora[1].pdf",
    "analysis_timestamp": "2025-09-15T18:57:28",
    "structure_preserved": false
  },
  "theme_analysis": {
    "ciencia": [
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 1538,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 5298,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 22.413793103448278,
        "position": 22826,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 24145,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 36967,
        "chapter": 9
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 43876,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 34.21052631578947,
        "position": 49817,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 52347,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 52.70270270270271,
        "position": 57533,
        "chapter": 14
      },
      {
        "segment": 1,
        "score": 27.083333333333336,
        "position": 121610,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 34.21052631578947,
        "position": 123110,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 159082,
        "chapter": 25
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 160538,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 72.22222222222221,
        "position": 161986,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 164653,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 169125,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 170590,
        "chapter": 6
      }
    ],
    "tecnologia": [
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 1538,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 52347,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 27.027027027027025,
        "position": 57533,
        "chapter": 14
      },
      {
        "segment": 1,
        "score": 20.833333333333336,
        "position": 121610,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 26.31578947368421,
        "position": 123110,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 27.77777777777778,
        "position": 161986,
        "chapter": 6
      }
    ],
    "filosofia": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 2634,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 75.0,
        "position": 3971,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 5298,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 6465,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 8545,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 77.58620689655173,
        "position": 22826,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 24145,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 25207,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 30217,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 38322,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 42566,
        "chapter": 10
      },
      {
        "segment": 1,
        "score": 69.76744186046511,
        "position": 43876,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 46824,
        "chapter": 11
      },
      {
        "segment": 1,
        "score": 39.473684210526315,
        "position": 49817,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 20.27027027027027,
        "position": 57533,
        "chapter": 14
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 58985,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 60489,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 63432,
        "chapter": 15
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 66119,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 68285,
        "chapter": 16
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 69618,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 95783,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 102989,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 31.25,
        "position": 121610,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 39.473684210526315,
        "position": 123110,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 147919,
        "chapter": 6
      }
    ],
    "arte": [
      {
        "segment": 1,
        "score": 25.0,
        "position": 3971,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 8545,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 48356,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 26.31578947368421,
        "position": 49817,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 60489,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 63432,
        "chapter": 15
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 71089,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 77486,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 104462,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 113210,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 114738,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 20.833333333333336,
        "position": 121610,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 128906,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 130360,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 134444,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 143430,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 149410,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 150970,
        "chapter": 6
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 36.936465721040186,
      "position": 266,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 1.6271455196384472e-05
    },
    {
      "segment": 1,
      "difficulty": 25.66295025728988,
      "position": 1538,
      "chapter": 1,
      "main_theme": "ciencia",
      "word_count": 159,
      "preservation_score": 1.5042056359324311e-05
    },
    {
      "segment": 1,
      "difficulty": 33.064216366158114,
      "position": 2634,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 206,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 33.211194029850745,
      "position": 3971,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 201,
      "preservation_score": 1.757317161209523e-05
    },
    {
      "segment": 1,
      "difficulty": 25.664159891598914,
      "position": 5298,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 164,
      "preservation_score": 1.3860869241364554e-05
    },
    {
      "segment": 1,
      "difficulty": 28.772727272727273,
      "position": 6465,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 220,
      "preservation_score": 2.306930758954065e-05
    },
    {
      "segment": 1,
      "difficulty": 24.881333333333334,
      "position": 7932,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 50,
      "preservation_score": 1.3499281348111564e-06
    },
    {
      "segment": 1,
      "difficulty": 34.693089430894304,
      "position": 8545,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 205,
      "preservation_score": 3.914791590952353e-05
    },
    {
      "segment": 1,
      "difficulty": 24.36875,
      "position": 9995,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 16,
      "preservation_score": 4.821171910039844e-08
    },
    {
      "segment": 1,
      "difficulty": 26.79108409321175,
      "position": 10237,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 3.555614283654386e-05
    },
    {
      "segment": 1,
      "difficulty": 36.91294466403162,
      "position": 11407,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 2.7336044729925913e-05
    },
    {
      "segment": 1,
      "difficulty": 32.31167557932264,
      "position": 12748,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 198,
      "preservation_score": 4.035320888703349e-05
    },
    {
      "segment": 1,
      "difficulty": 22.51449067431851,
      "position": 14120,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 205,
      "preservation_score": 4.117280811174026e-05
    },
    {
      "segment": 1,
      "difficulty": 22.38962765957447,
      "position": 15530,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 2.8203855673733093e-05
    },
    {
      "segment": 1,
      "difficulty": 21.605,
      "position": 16774,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 180,
      "preservation_score": 4.1992407336447044e-05
    },
    {
      "segment": 1,
      "difficulty": 24.87466063348416,
      "position": 18070,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "segment": 1,
      "difficulty": 34.09,
      "position": 19480,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 70,
      "preservation_score": 2.6516445505219144e-06
    },
    {
      "segment": 1,
      "difficulty": 34.004285714285714,
      "position": 20072,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 210,
      "preservation_score": 2.2948778291789653e-05
    },
    {
      "segment": 1,
      "difficulty": 38.6,
      "position": 21481,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 2.0248922022167342e-05
    },
    {
      "segment": 1,
      "difficulty": 31.427966101694913,
      "position": 22826,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 177,
      "preservation_score": 2.2780037274938265e-05
    },
    {
      "segment": 1,
      "difficulty": 36.5527027027027,
      "position": 24145,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 148,
      "preservation_score": 1.3740339943613556e-05
    },
    {
      "segment": 1,
      "difficulty": 36.401818181818186,
      "position": 25207,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 220,
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "segment": 1,
      "difficulty": 42.55393258426966,
      "position": 26602,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 89,
      "preservation_score": 4.62832503363825e-06
    },
    {
      "segment": 1,
      "difficulty": 25.38751629726206,
      "position": 27304,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 236,
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "segment": 1,
      "difficulty": 36.48938053097345,
      "position": 28723,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 226,
      "preservation_score": 2.2370237662584875e-05
    },
    {
      "segment": 1,
      "difficulty": 35.918297872340425,
      "position": 30217,
      "chapter": 7,
      "main_theme": "filosofia",
      "word_count": 235,
      "preservation_score": 2.796279707823109e-05
    },
    {
      "segment": 1,
      "difficulty": 34.056289308176105,
      "position": 31710,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 106,
      "preservation_score": 8.388839123469328e-06
    },
    {
      "segment": 1,
      "difficulty": 33.80451127819549,
      "position": 32457,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 228,
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "segment": 1,
      "difficulty": 34.98016194331984,
      "position": 33934,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 247,
      "preservation_score": 2.6034328314215155e-05
    },
    {
      "segment": 1,
      "difficulty": 36.80544554455446,
      "position": 35495,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.5668808707629495e-05
    },
    {
      "segment": 1,
      "difficulty": 33.32442244224423,
      "position": 36967,
      "chapter": 9,
      "main_theme": "ciencia",
      "word_count": 202,
      "preservation_score": 2.2948778291789653e-05
    },
    {
      "segment": 1,
      "difficulty": 26.876960784313724,
      "position": 38322,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 204,
      "preservation_score": 1.7549065752545035e-05
    },
    {
      "segment": 1,
      "difficulty": 36.42,
      "position": 39578,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 240,
      "preservation_score": 3.145814671300998e-05
    },
    {
      "segment": 1,
      "difficulty": 34.727526395173456,
      "position": 41099,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 2.656465722431953e-05
    },
    {
      "segment": 1,
      "difficulty": 30.794456289978676,
      "position": 42566,
      "chapter": 10,
      "main_theme": "filosofia",
      "word_count": 201,
      "preservation_score": 1.942932279746057e-05
    },
    {
      "segment": 1,
      "difficulty": 31.101968085106382,
      "position": 43876,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 235,
      "preservation_score": 3.07590767860542e-05
    },
    {
      "segment": 1,
      "difficulty": 35.48679245283019,
      "position": 45366,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 212,
      "preservation_score": 1.388497510091475e-05
    },
    {
      "segment": 1,
      "difficulty": 31.95719489981785,
      "position": 46824,
      "chapter": 11,
      "main_theme": "filosofia",
      "word_count": 244,
      "preservation_score": 3.0060006859098423e-05
    },
    {
      "segment": 1,
      "difficulty": 33.94101382488479,
      "position": 48356,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 217,
      "preservation_score": 2.2370237662584875e-05
    },
    {
      "segment": 1,
      "difficulty": 36.31739130434782,
      "position": 49817,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 138,
      "preservation_score": 9.642343820079688e-06
    },
    {
      "segment": 1,
      "difficulty": 36.52602739726028,
      "position": 50866,
      "chapter": 12,
      "main_theme": "none",
      "word_count": 219,
      "preservation_score": 2.656465722431953e-05
    },
    {
      "segment": 1,
      "difficulty": 31.85397196261682,
      "position": 52347,
      "chapter": 2,
      "main_theme": "ciencia",
      "word_count": 214,
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "segment": 1,
      "difficulty": 24.21875,
      "position": 53762,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 16,
      "preservation_score": 2.410585955019922e-08
    },
    {
      "segment": 1,
      "difficulty": 42.577319587628864,
      "position": 54150,
      "chapter": 13,
      "main_theme": "none",
      "word_count": 194,
      "preservation_score": 1.822402981995061e-05
    },
    {
      "segment": 1,
      "difficulty": 36.40243902439025,
      "position": 55512,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 246,
      "preservation_score": 2.656465722431953e-05
    },
    {
      "segment": 1,
      "difficulty": 23.5,
      "position": 57058,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 28,
      "preservation_score": 4.3390547190358593e-07
    },
    {
      "segment": 1,
      "difficulty": 36.44776785714286,
      "position": 57533,
      "chapter": 14,
      "main_theme": "ciencia",
      "word_count": 224,
      "preservation_score": 1.822402981995061e-05
    },
    {
      "segment": 1,
      "difficulty": 35.62245762711864,
      "position": 58985,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 236,
      "preservation_score": 2.1671167735629094e-05
    },
    {
      "segment": 1,
      "difficulty": 36.46891891891892,
      "position": 60489,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 222,
      "preservation_score": 1.8175818100850208e-05
    },
    {
      "segment": 1,
      "difficulty": 38.5,
      "position": 61944,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 223,
      "preservation_score": 3.0060006859098423e-05
    },
    {
      "segment": 1,
      "difficulty": 37.412328767123284,
      "position": 63432,
      "chapter": 15,
      "main_theme": "filosofia",
      "word_count": 219,
      "preservation_score": 2.1478320859227506e-05
    },
    {
      "segment": 1,
      "difficulty": 31.00972906403941,
      "position": 64831,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 203,
      "preservation_score": 2.1936332190681292e-05
    },
    {
      "segment": 1,
      "difficulty": 38.425,
      "position": 66119,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 232,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 36.49325842696629,
      "position": 67602,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 89,
      "preservation_score": 2.3864800954697224e-06
    },
    {
      "segment": 1,
      "difficulty": 31.173648648648648,
      "position": 68285,
      "chapter": 16,
      "main_theme": "filosofia",
      "word_count": 222,
      "preservation_score": 2.343089548279364e-05
    },
    {
      "segment": 1,
      "difficulty": 35.374493927125506,
      "position": 69618,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 247,
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "segment": 1,
      "difficulty": 37.30642201834863,
      "position": 71089,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 218,
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "segment": 1,
      "difficulty": 35.134,
      "position": 72469,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 75,
      "preservation_score": 1.7356218876143437e-06
    },
    {
      "segment": 1,
      "difficulty": 38.37973568281939,
      "position": 73044,
      "chapter": 17,
      "main_theme": "none",
      "word_count": 227,
      "preservation_score": 1.6199137617733874e-05
    },
    {
      "segment": 1,
      "difficulty": 35.510931174089066,
      "position": 74462,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 247,
      "preservation_score": 1.8874888027805986e-05
    },
    {
      "segment": 1,
      "difficulty": 36.38414634146341,
      "position": 75959,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 246,
      "preservation_score": 2.965020724674504e-05
    },
    {
      "segment": 1,
      "difficulty": 36.33754940711462,
      "position": 77486,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 253,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 38.18139880952381,
      "position": 79016,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 224,
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "segment": 1,
      "difficulty": 29.70254524886878,
      "position": 80516,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 36.00408163265306,
      "position": 81926,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 147,
      "preservation_score": 1.4318880572818336e-05
    },
    {
      "segment": 1,
      "difficulty": 38.42434782608696,
      "position": 83114,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "segment": 1,
      "difficulty": 37.368421052631575,
      "position": 84583,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 228,
      "preservation_score": 2.343089548279364e-05
    },
    {
      "segment": 1,
      "difficulty": 36.326459143968876,
      "position": 85995,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 257,
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "segment": 1,
      "difficulty": 22.723076923076924,
      "position": 87549,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 13,
      "preservation_score": 7.231757865059766e-08
    },
    {
      "segment": 1,
      "difficulty": 37.87692307692308,
      "position": 87768,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 234,
      "preservation_score": 2.092388608957292e-05
    },
    {
      "segment": 1,
      "difficulty": 36.26083333333333,
      "position": 89223,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 240,
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "segment": 1,
      "difficulty": 35.86022408963585,
      "position": 90702,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "segment": 1,
      "difficulty": 36.19375,
      "position": 92138,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 96,
      "preservation_score": 2.6516445505219144e-06
    },
    {
      "segment": 1,
      "difficulty": 36.278,
      "position": 92767,
      "chapter": 20,
      "main_theme": "none",
      "word_count": 250,
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "segment": 1,
      "difficulty": 36.37738095238095,
      "position": 94227,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 252,
      "preservation_score": 2.314162516819125e-05
    },
    {
      "segment": 1,
      "difficulty": 36.38612244897959,
      "position": 95783,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 245,
      "preservation_score": 2.796279707823109e-05
    },
    {
      "segment": 1,
      "difficulty": 36.46649746192894,
      "position": 97307,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 197,
      "preservation_score": 2.1984543909781684e-05
    },
    {
      "segment": 1,
      "difficulty": 39.438235294117646,
      "position": 98616,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 2.9360936932142646e-05
    },
    {
      "segment": 1,
      "difficulty": 33.897873754152826,
      "position": 100143,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 215,
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "segment": 1,
      "difficulty": 32.08233944954128,
      "position": 101559,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 218,
      "preservation_score": 3.577309557249564e-05
    },
    {
      "segment": 1,
      "difficulty": 38.38559322033898,
      "position": 102989,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 236,
      "preservation_score": 1.8874888027805986e-05
    },
    {
      "segment": 1,
      "difficulty": 36.361176470588234,
      "position": 104462,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 255,
      "preservation_score": 2.3864800954697227e-05
    },
    {
      "segment": 1,
      "difficulty": 30.642212924221294,
      "position": 106022,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 239,
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "segment": 1,
      "difficulty": 36.39620253164557,
      "position": 107494,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 237,
      "preservation_score": 1.822402981995061e-05
    },
    {
      "segment": 1,
      "difficulty": 31.971883116883117,
      "position": 108978,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 220,
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "segment": 1,
      "difficulty": 36.36746987951807,
      "position": 110374,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 249,
      "preservation_score": 2.796279707823109e-05
    },
    {
      "segment": 1,
      "difficulty": 36.415346534653466,
      "position": 111905,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.967038139296256e-05
    },
    {
      "segment": 1,
      "difficulty": 36.557847533632284,
      "position": 113210,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 223,
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "segment": 1,
      "difficulty": 37.409459459459455,
      "position": 114738,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 222,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 35.505976095617534,
      "position": 116152,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 251,
      "preservation_score": 2.306930758954065e-05
    },
    {
      "segment": 1,
      "difficulty": 24.135645604395606,
      "position": 117692,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 3.104834710065659e-05
    },
    {
      "segment": 1,
      "difficulty": 35.709199999999996,
      "position": 119084,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 250,
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "segment": 1,
      "difficulty": 30.13607843137255,
      "position": 120574,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 170,
      "preservation_score": 1.1088695393091642e-05
    },
    {
      "segment": 1,
      "difficulty": 33.46975493126121,
      "position": 121610,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 239,
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "segment": 1,
      "difficulty": 35.54141193595342,
      "position": 123110,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 229,
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "segment": 1,
      "difficulty": 36.44434389140271,
      "position": 124599,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 33.39915966386555,
      "position": 126031,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "segment": 1,
      "difficulty": 30.9125,
      "position": 127525,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 216,
      "preservation_score": 2.9698418965845438e-05
    },
    {
      "segment": 1,
      "difficulty": 29.378205128205128,
      "position": 128906,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 234,
      "preservation_score": 3.172331116806217e-05
    },
    {
      "segment": 1,
      "difficulty": 21.218556701030927,
      "position": 130360,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 194,
      "preservation_score": 2.883060802203827e-05
    },
    {
      "segment": 1,
      "difficulty": 32.72744853399875,
      "position": 131590,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 229,
      "preservation_score": 2.5648634561411964e-05
    },
    {
      "segment": 1,
      "difficulty": 35.079613095238095,
      "position": 133015,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 224,
      "preservation_score": 2.699856269622312e-05
    },
    {
      "segment": 1,
      "difficulty": 36.41842105263158,
      "position": 134444,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 228,
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "segment": 1,
      "difficulty": 30.431696428571428,
      "position": 135898,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 224,
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "segment": 1,
      "difficulty": 36.407391304347826,
      "position": 137494,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "segment": 1,
      "difficulty": 36.30996015936255,
      "position": 138951,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 251,
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "segment": 1,
      "difficulty": 32.865725806451614,
      "position": 140445,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 248,
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "segment": 1,
      "difficulty": 36.32520661157025,
      "position": 141969,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 242,
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "segment": 1,
      "difficulty": 35.46035242290749,
      "position": 143430,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 227,
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "segment": 1,
      "difficulty": 42.36153846153846,
      "position": 144910,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 247,
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "segment": 1,
      "difficulty": 38.3698347107438,
      "position": 146426,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 242,
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "segment": 1,
      "difficulty": 40.43047210300429,
      "position": 147919,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 233,
      "preservation_score": 3.07590767860542e-05
    },
    {
      "segment": 1,
      "difficulty": 34.618631178707226,
      "position": 149410,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 263,
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "segment": 1,
      "difficulty": 27.68695652173913,
      "position": 150970,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 207,
      "preservation_score": 1.6922313404239855e-05
    },
    {
      "segment": 1,
      "difficulty": 31.051923076923078,
      "position": 152246,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 234,
      "preservation_score": 3.2157216639965757e-05
    },
    {
      "segment": 1,
      "difficulty": 36.386250000000004,
      "position": 153741,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 240,
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "segment": 1,
      "difficulty": 31.639666666666667,
      "position": 155237,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 225,
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "segment": 1,
      "difficulty": 38.27789878283152,
      "position": 156749,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 223,
      "preservation_score": 2.0827462651372127e-05
    },
    {
      "segment": 1,
      "difficulty": 26.899479166666666,
      "position": 158121,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 128,
      "preservation_score": 5.954147308899207e-06
    },
    {
      "segment": 1,
      "difficulty": 36.52511627906976,
      "position": 159082,
      "chapter": 25,
      "main_theme": "ciencia",
      "word_count": 215,
      "preservation_score": 1.349928134811156e-05
    },
    {
      "segment": 1,
      "difficulty": 35.04009009009009,
      "position": 160538,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 222,
      "preservation_score": 2.0248922022167342e-05
    },
    {
      "segment": 1,
      "difficulty": 29.985714285714288,
      "position": 161986,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 189,
      "preservation_score": 1.6874101685139456e-05
    },
    {
      "segment": 1,
      "difficulty": 31.006140350877192,
      "position": 163258,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 228,
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "segment": 1,
      "difficulty": 36.45810810810811,
      "position": 164653,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 222,
      "preservation_score": 1.822402981995061e-05
    },
    {
      "segment": 1,
      "difficulty": 36.40246913580247,
      "position": 166100,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 243,
      "preservation_score": 3.145814671300998e-05
    },
    {
      "segment": 1,
      "difficulty": 36.44439655172414,
      "position": 167626,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 232,
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "segment": 1,
      "difficulty": 30.608057851239668,
      "position": 169125,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 242,
      "preservation_score": 2.306930758954065e-05
    },
    {
      "segment": 1,
      "difficulty": 36.8910480349345,
      "position": 170590,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 229,
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "segment": 1,
      "difficulty": 28.831060606060607,
      "position": 172069,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 198,
      "preservation_score": 1.9525746235661365e-05
    },
    {
      "segment": 1,
      "difficulty": 23.133490566037736,
      "position": 173379,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 106,
      "preservation_score": 8.244203966168133e-06
    },
    {
      "segment": 1,
      "difficulty": 31.5778,
      "position": 174325,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 250,
      "preservation_score": 2.092388608957292e-05
    },
    {
      "segment": 1,
      "difficulty": 38.347457627118644,
      "position": 175766,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 236,
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "segment": 1,
      "difficulty": 37.90218253968254,
      "position": 177208,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 216,
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "segment": 1,
      "difficulty": 33.1823693379791,
      "position": 178632,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 205,
      "preservation_score": 2.2129179067082882e-05
    },
    {
      "segment": 1,
      "difficulty": 33.430647709320695,
      "position": 180037,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 211,
      "preservation_score": 1.757317161209523e-05
    },
    {
      "segment": 1,
      "difficulty": 31.88480392156863,
      "position": 181400,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 204,
      "preservation_score": 3.442316743768448e-05
    },
    {
      "segment": 1,
      "difficulty": 26.308678343949044,
      "position": 182807,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 157,
      "preservation_score": 1.5042056359324311e-05
    },
    {
      "segment": 1,
      "difficulty": 36.571641791044776,
      "position": 183896,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 201,
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "segment": 1,
      "difficulty": 28.649742268041237,
      "position": 185298,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 97,
      "preservation_score": 4.700642612288848e-06
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Preconceito quântico  \\n \\nDevemos nos questionar como o preconceito e o \\npré-conceito são concebidos. Quais são as \\ndiferenças e motivos dessa concepção de juízo de \\nvalores; como surgiu o início dos nossos \\nestereótipos preconceituosos?  \\nTudo em nossa vida são valores construídos de \\nacordo com o que vivemos, porém o que vivemos \\né certo ou errado? O que é certo ou errado? São \\nperguntas atrás de perguntas até chegarmos a \\numa indecisão constante e construtiva dos nosso \\npróprios porquês. Como assim, os nossos própri os \\nporquês? Nós, humanos, evoluímos de acordo \\ncom a nossa ganância de ser mais, ter mais, ser \\nmelhor, mais bonito, melhor jogador de futebol, \\nmelhor empresário. Independente do \\ndirecionamento da vida de cada um, o seu desejo \\nde ambição ou ganância varia de  acordo com a \\nprópria necessidade, o seu estilo de vida  de \\nacordo com seu DNA mais o meio em que você \\nvive, fazendo você criar preconceito ou pré-\\nconceitos  devido a uma evolução humana \\ndesgovernada no aprendizado de caos e \\nadaptação, em consequência de sua  própria \\nignorância de não saber viver um para com o \\noutro.  \\nEternidade é a grande busca dos humanos!",
      "position": 266,
      "chapter": 1,
      "page": 2,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.936465721040186,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 20.88888888888889,
        "avg_word_length": 4.973404255319149,
        "unique_word_ratio": 0.6276595744680851,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.12234042553191489,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "acordo",
          "mais",
          "preconceito",
          "como",
          "vida",
          "melhor",
          "valores",
          "nossos",
          "nossa",
          "vivemos",
          "certo",
          "errado",
          "perguntas",
          "porquês",
          "humanos",
          "ganância",
          "própria",
          "você",
          "quântico",
          "devemos"
        ],
        "entities": [
          [
            "Preconceito",
            "PERSON"
          ],
          [
            "Devemos",
            "PERSON"
          ],
          [
            "dessa concepção",
            "PERSON"
          ],
          [
            "como surgiu",
            "PERSON"
          ],
          [
            "de perguntas",
            "ORG"
          ],
          [
            "porquês",
            "PERSON"
          ],
          [
            "evoluímos de acordo",
            "PERSON"
          ],
          [
            "ganância de ser mais",
            "PERSON"
          ],
          [
            "mais bonito",
            "PERSON"
          ],
          [
            "melhor",
            "GPE"
          ]
        ],
        "readability_score": 88.0635342789598,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 118,
        "lexical_diversity": 0.6276595744680851
      },
      "preservation_score": 1.6271455196384472e-05
    },
    {
      "id": 1,
      "text": "Por quais  motivos  precisamos de Deuses?  \\nPor qua is motivos  buscamos respostas?  \\nPor quais  motivo s criamos tecnologias?  \\nÚnica certeza que temos sobre o univer so é que \\nele foi gerado através de uma grande liberação de \\nenergia (valor quântico)  e, através desse \\nquestionamento sem resposta e com muitas \\nrespostas extremistas, queremos saber quem \\noriginou... Já se perguntou : se essa origem possa \\nter sido um de nós?  \\nEsse mesmo que é semelhante a nós, é eterno ? \\nNós somos eternos?  \\nQual é a procura que nós humanos queremos \\nachar?  \\n“Todos nós temos compromissos para com o \\nplaneta Terra, pois dela nós viemos e para ela nós \\nvoltaremos. ” \\nTemos que ter compromisso e responsab ilidade \\nde sermos responsáveis pelas nossas falhas \\ngananciosas e miseráveis , todos viemos de falhas \\npassadas, se viemos de falhas passadas por quais \\nmotivos mantemos as falhas?  \\nTodos nós temos uma origem, dentro dessa \\norigem, qual é a  estrutura familiar a qual eu \\ntenho?",
      "position": 1538,
      "chapter": 1,
      "page": 3,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 25.66295025728988,
      "complexity_metrics": {
        "word_count": 159,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 14.454545454545455,
        "avg_word_length": 4.937106918238993,
        "unique_word_ratio": 0.7044025157232704,
        "avg_paragraph_length": 159.0,
        "punctuation_density": 0.13836477987421383,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "falhas",
          "quais",
          "motivos",
          "origem",
          "qual",
          "todos",
          "viemos",
          "respostas",
          "através",
          "queremos",
          "passadas",
          "precisamos",
          "deuses",
          "buscamos",
          "motivo",
          "criamos",
          "tecnologias",
          "única",
          "certeza"
        ],
        "entities": [
          [
            "precisamos de Deuses",
            "PERSON"
          ],
          [
            "motivo s criamos",
            "ORG"
          ],
          [
            "queremos",
            "PERSON"
          ],
          [
            "Já se",
            "PERSON"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "nós viemos",
            "FAC"
          ],
          [
            "para ela nós \\nvoltaremos",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "nossas",
            "PERSON"
          ],
          [
            "todos viemos de falhas \\npassadas",
            "PERSON"
          ]
        ],
        "readability_score": 91.29159519725557,
        "semantic_density": 0,
        "word_count": 159,
        "unique_words": 112,
        "lexical_diversity": 0.7044025157232704
      },
      "preservation_score": 1.5042056359324311e-05
    },
    {
      "id": 1,
      "text": "Em uma escala que o seu nascimento seja \\ncorrelacionado a filho de  uma pessoa viciada em \\ncrack , seja 1 , e uma pessoa filho de  alguém com \\nmuito dinheiro ao ponto de nunca pensar na \\nfome como 5, sendo que, durante o trajeto da \\nvida, nós podemos  atingir o nível 10 como \\nfelicidade suprema a qual não se tem remorsos \\npelo que viveu e uma plenitude em satisfação \\ncom a  própria vida sendo a maior escala.  \\nPara termos essa magnitude de vida,  o que  \\nprecisamos ter ? um trajeto perfeito.  \\n“Logo essa vida não existe, até porque, única \\nperfeição que eu escuto falar é a divindade \\nchamada Deus. ” \\nQuando somos crianças nós só temos o \\ncompromisso de sermos crianças, assim \\npercebemos a pureza estar em não ter  \\ncompromisso com a obrigação e sim com a vida. \\nPorém quando começamos a ter obrigação em \\ntermos compromissos , sejamos comprometidos \\npara sermos de confiança, até porque, essa \\nconfiança é aquela que nos motiva  a vivermos em \\num prol do planeta  Terra!  \\nNós, até hoje, estamos no processo de \\naprendizado do caos, efeito e adaptação, pela \\nquestão da própria sobrevivência, nos tornando \\npessoas cheias de regras “desnecessárias”, em \\nrazão da própria incapacidade de se adaptar em \\nsociedade.",
      "position": 2634,
      "chapter": 1,
      "page": 4,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 33.064216366158114,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.428571428571427,
        "avg_word_length": 4.737864077669903,
        "unique_word_ratio": 0.6456310679611651,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.12135922330097088,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "própria",
          "essa",
          "escala",
          "seja",
          "filho",
          "pessoa",
          "como",
          "sendo",
          "trajeto",
          "termos",
          "porque",
          "quando",
          "crianças",
          "compromisso",
          "sermos",
          "obrigação",
          "confiança",
          "nascimento",
          "correlacionado"
        ],
        "entities": [
          [
            "1",
            "CARDINAL"
          ],
          [
            "muito dinheiro",
            "PERSON"
          ],
          [
            "ponto de nunca",
            "ORG"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "nós podemos  atingir o",
            "ORG"
          ],
          [
            "10",
            "CARDINAL"
          ],
          [
            "remorsos \\npelo",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Porém",
            "NORP"
          ],
          [
            "sejamos",
            "PERSON"
          ]
        ],
        "readability_score": 83.86435506241332,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 133,
        "lexical_diversity": 0.6456310679611651
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "No Egito antigo, por exemplo, a necessidade de \\nconstruir pirâmides para “canaliz ar a energia do \\nmundo” gerou caos em quantidade de escravos e \\nmortes pela própria ganância de ser maior, ter \\nmais, nos fazendo ter uma evolução sobre \\nconstruções, espiritualidade, império, exército e \\nmuitas outras coisas devido a sua própria \\nganância.  \\nA Gr écia nos fez entender sobre a luxúria de se \\nviver — os deuses magníficos, as construções \\nbelas, o exaltar a arte e a filosofia.  \\nA Palestina foi o caos ao constituir uma \\nespiritualidade de “exageros”, devido a própria \\nnecessidade de se crer em algo, os torn ando \\nextremistas em ter milagre, para sobreviver ao \\nmeio em que a vida foi destruída pelo próprio \\nviver.  \\nEm Roma houve um avanço na ordem política da \\npopulação, devido a uma necessidade de controle \\nde caos para poder viver.  \\nA Segunda guerra mundial foi uma  guerra entre \\neu ser superior por ser de “uma espécie”, criando \\ncaos e adaptação evolutiva em função de ser mais \\ninteligente que o outro, nos fazendo ter uma \\nevolução tecnológica devido à necessidade de \\ncontrolar o nosso próprio caos.  \\nEsse texto é uma pequ ena explicação sobre uma \\nconstrução de pensamento que será a base desse",
      "position": 3971,
      "chapter": 1,
      "page": 5,
      "segment_type": "page",
      "themes": {
        "filosofia": 75.0,
        "arte": 25.0
      },
      "difficulty": 33.211194029850745,
      "complexity_metrics": {
        "word_count": 201,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 33.5,
        "avg_word_length": 4.870646766169155,
        "unique_word_ratio": 0.6318407960199005,
        "avg_paragraph_length": 201.0,
        "punctuation_density": 0.09950248756218906,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "necessidade",
          "devido",
          "própria",
          "viver",
          "ganância",
          "mais",
          "fazendo",
          "evolução",
          "construções",
          "espiritualidade",
          "próprio",
          "guerra",
          "egito",
          "antigo",
          "exemplo",
          "construir",
          "pirâmides",
          "canaliz",
          "energia"
        ],
        "entities": [
          [
            "Egito",
            "PERSON"
          ],
          [
            "própria ganância de ser",
            "PERSON"
          ],
          [
            "magníficos",
            "PERSON"
          ],
          [
            "política da \\npopulação",
            "PERSON"
          ],
          [
            "Segunda",
            "PRODUCT"
          ],
          [
            "de ser mais \\ninteligente",
            "PERSON"
          ],
          [
            "tecnológica",
            "GPE"
          ]
        ],
        "readability_score": 81.78880597014926,
        "semantic_density": 0,
        "word_count": 201,
        "unique_words": 127,
        "lexical_diversity": 0.6318407960199005
      },
      "preservation_score": 1.757317161209523e-05
    },
    {
      "id": 1,
      "text": "livro de forma construtiva, de criarmos regras \\nsobre regras perante o nosso próprio caos, pela \\nincapacidade de não conter o nosso  próprio ego.  \\n \\nAfinal, nós estamos falando sobre o quê?  \\nOnde está o quântico?  \\nComo funciona o quântico?  \\nO que nós somos?  \\nNós somos feitos de corpo e mente. Dentro desse \\ncorpo, temos o metabolismo, esse metabolismo é \\na medição da sua energia corpórea, trazida pelo \\nseu DNA através de entrelaçamento s evolutiv os \\nde uma linha de tempo familiar; temos a evolução \\nquântica dentro da  nossa própria mente, nós \\ntemos a consciência e o subconsciente \\ninterligados ao metabolismo, criando uma \\nimportância de energia mental e corpórea \\nproporcional ao nosso  próprio DNA, de valores \\nevolutivos da nossa  própria linha de tempo.  \\nNosso corpo e a noss a mente têm um gasto de \\nenergia proporcional ao nosso  metabolismo de \\nacordo com a nossa  própria necessidade de \\nconsumo.  \\nAlzheimer e ELA (Esclerose lateral amiotrófica), \\npor exemplo, são doenças de falta de energia \\nmental e corpórea respectivamente.",
      "position": 5298,
      "chapter": 1,
      "page": 6,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 25.664159891598914,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 18.22222222222222,
        "avg_word_length": 5.176829268292683,
        "unique_word_ratio": 0.6280487804878049,
        "avg_paragraph_length": 164.0,
        "punctuation_density": 0.12804878048780488,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "metabolismo",
          "energia",
          "próprio",
          "corpo",
          "mente",
          "temos",
          "corpórea",
          "nossa",
          "própria",
          "regras",
          "quântico",
          "somos",
          "dentro",
          "linha",
          "tempo",
          "mental",
          "proporcional",
          "livro",
          "forma"
        ],
        "entities": [
          [
            "livro de forma construtiva",
            "PERSON"
          ],
          [
            "incapacidade de não",
            "PERSON"
          ],
          [
            "próprio ego",
            "PERSON"
          ],
          [
            "Afinal",
            "ORG"
          ],
          [
            "nós estamos",
            "ORG"
          ],
          [
            "falando sobre",
            "ORG"
          ],
          [
            "quê",
            "PERSON"
          ],
          [
            "Dentro",
            "LOC"
          ],
          [
            "corpórea",
            "GPE"
          ],
          [
            "trazida pelo \\nseu",
            "PERSON"
          ]
        ],
        "readability_score": 89.33584010840109,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 103,
        "lexical_diversity": 0.6280487804878049
      },
      "preservation_score": 1.3860869241364554e-05
    },
    {
      "id": 1,
      "text": "Nossa m ente é a captação e armazenamento de \\nenergia da nossa própria vida, com valores \\nrelativos a nossa própria existência, de acordo \\ncom a nossa própria necessidade corpórea e \\nmental, com gastos de energia proporcionais, \\nentre a mente e o corpo, do nosso própri o \\nmetabolismo. No decorrer do tempo (marcação \\nda propagação da energia) da nossa existência, \\nnós agregamos mais energia, nos fazendo ter um \\nmaior gasto da nossa própria energia para se ter \\nacesso à nossa própria vida. Quanto mais velhos \\nnós ficamos, menos energia (metabolismo) nós \\ntemos e mais energia precisamos, devido ao \\nacúmulo de lembranças de uma vida, nos fazendo \\nnão ter energia suficiente para acessar a \\nlembrança necessária para se viver. A falta de \\nenergia mental nos faz ter menos acesso a nossa \\nprópria vida, fazendo, assim, termos lembranças \\navulsos  e incoerentes, devido a falta da nossa \\nprópria energia, gerando escassez ou \\ndissimulação das nossas próprias lembranças, o \\nque ocorre em pessoas com Alzheimer.  \\nNosso corpo precisa de energia para funcion ar: \\nver, falar, ouvir, sentir, andar, movimentar. O \\nexcesso de energia corpórea nos faz sermos  \\natletas e a falta de energia corpórea nos faz ter \\nELA.  \\nEsses exemplos são uma forma de se entender a \\ndiferença entre o corpo e a mente diante da \\nnossa própria en ergia. Nossa mente é o mundo",
      "position": 6465,
      "chapter": 1,
      "page": 7,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.772727272727273,
      "complexity_metrics": {
        "word_count": 220,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.5,
        "avg_word_length": 5.0,
        "unique_word_ratio": 0.5409090909090909,
        "avg_paragraph_length": 220.0,
        "punctuation_density": 0.1318181818181818,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "nossa",
          "própria",
          "vida",
          "corpórea",
          "mente",
          "corpo",
          "mais",
          "fazendo",
          "lembranças",
          "falta",
          "existência",
          "mental",
          "entre",
          "nosso",
          "metabolismo",
          "acesso",
          "menos",
          "devido",
          "ente"
        ],
        "entities": [
          [
            "Nossa",
            "PERSON"
          ],
          [
            "de acordo",
            "PERSON"
          ],
          [
            "nós agregamos mais",
            "ORG"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "nossa própria",
            "PERSON"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "nós ficamos",
            "GPE"
          ],
          [
            "devido ao \\nacúmulo de lembranças de uma vida",
            "PERSON"
          ],
          [
            "para se viver",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 84.75,
        "semantic_density": 0,
        "word_count": 220,
        "unique_words": 119,
        "lexical_diversity": 0.5409090909090909
      },
      "preservation_score": 2.306930758954065e-05
    },
    {
      "id": 1,
      "text": "quântico, pois nela não há gravidade e tempo. \\nTodas as nossas lembranças são onipresentes, \\ntodas as nossas lembranças são linhas de \\nraciocínio (entrelaçamento quântico) de acordo \\ncom o nosso próprio viver, junto ao nosso corpo \\nfísico.  \\nNosso corpo é a junção perfeita da física quântica \\ne a física do físico!",
      "position": 7932,
      "chapter": 1,
      "page": 8,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.881333333333334,
      "complexity_metrics": {
        "word_count": 50,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 16.666666666666668,
        "avg_word_length": 5.16,
        "unique_word_ratio": 0.8,
        "avg_paragraph_length": 50.0,
        "punctuation_density": 0.12,
        "line_break_count": 7,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "quântico",
          "todas",
          "nossas",
          "lembranças",
          "corpo",
          "físico",
          "física",
          "pois",
          "nela",
          "gravidade",
          "tempo",
          "onipresentes",
          "linhas",
          "raciocínio",
          "entrelaçamento",
          "acordo",
          "próprio",
          "viver",
          "junto"
        ],
        "entities": [
          [
            "nela",
            "GPE"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "nossas lembranças",
            "PERSON"
          ],
          [
            "nossas lembranças são linhas de \\nraciocínio",
            "ORG"
          ]
        ],
        "readability_score": 90.11866666666667,
        "semantic_density": 0,
        "word_count": 50,
        "unique_words": 40,
        "lexical_diversity": 0.8
      },
      "preservation_score": 1.3499281348111564e-06
    },
    {
      "id": 1,
      "text": "Capítulo 1 Humano  \\nNós, humanos, (relativo ao homem ou próprio de \\nsua natureza. Etimologia: Humānus , a, um \\n‘próprio do homem, bondoso, erudito) somos \\nseres desenvolvidos devid o à necessidade de \\nsobrevivência, como consequência dessa \\nnecessidade, começamos a criar hábitos, \\ncostumes, paixões, afetos, sonhos. Dentro dessa \\nnecessidade de sobreviver diante do caos, \\ntivemos que nos agrupar e conviver uns com os \\noutros, assim, começam os a criar regras de \\nconvivência para sobreviver. Quando concebemos \\nregras, estabelecemos uma pirâmide de comando \\ne poder (possuir força física ou moral; ter \\ninfluência, valimento. Etimologia: originou a partir \\ndo latim possum , que significa “ser capaz de” ) de \\n“eu quero ser mais, eu posso ser mais, quem tem \\no direito de ser mais, meu filho pode mais”, o que \\ngerou discriminação (ação ou efeito de separar, \\nsegregar, pôr à parte) pela própria necessidade \\nde se ter regras (aquilo que regula, dirige, rege, \\npara se viver melhor, norma, fórmula que indica o \\nmodo apropriado de falar, pensar, agir em \\ndeterminados casos) para conseguir ter comida, \\nsegurança, calor, sexo, felicidade e todos os \\nnossos princípios básicos de sobrevivência.  \\nNa necessidade de viver um para com o outro, \\ngeramos sons referentes a coisas materiais e \\nsentimentais, esses mesmos sons materiais e",
      "position": 8545,
      "chapter": 1,
      "page": 10,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 34.693089430894304,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.166666666666664,
        "avg_word_length": 5.365853658536586,
        "unique_word_ratio": 0.7268292682926829,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.21951219512195122,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "mais",
          "regras",
          "homem",
          "próprio",
          "etimologia",
          "sobrevivência",
          "dessa",
          "criar",
          "sobreviver",
          "viver",
          "sons",
          "materiais",
          "capítulo",
          "humano",
          "humanos",
          "relativo",
          "natureza",
          "bondoso",
          "erudito"
        ],
        "entities": [
          [
            "próprio de \\nsua",
            "ORG"
          ],
          [
            "Etimologia",
            "GPE"
          ],
          [
            "paixões",
            "PERSON"
          ],
          [
            "tivemos que",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "ser mais",
            "PERSON"
          ],
          [
            "eu posso",
            "PERSON"
          ],
          [
            "pela própria",
            "PERSON"
          ],
          [
            "dirige",
            "GPE"
          ],
          [
            "para se viver melhor",
            "PERSON"
          ]
        ],
        "readability_score": 81.3069105691057,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 149,
        "lexical_diversity": 0.7268292682926829
      },
      "preservation_score": 3.914791590952353e-05
    },
    {
      "id": 1,
      "text": "sentimentais vêm de uma origem de valores \\nrelativos a um peso, de acordo com sua origem.",
      "position": 9995,
      "chapter": 1,
      "page": 11,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.36875,
      "complexity_metrics": {
        "word_count": 16,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 16.0,
        "avg_word_length": 4.5625,
        "unique_word_ratio": 0.875,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.125,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "origem",
          "sentimentais",
          "valores",
          "relativos",
          "peso",
          "acordo"
        ],
        "entities": [
          [
            "sentimentais",
            "ORG"
          ]
        ],
        "readability_score": 90.63125,
        "semantic_density": 0,
        "word_count": 16,
        "unique_words": 14,
        "lexical_diversity": 0.875
      },
      "preservation_score": 4.821171910039844e-08
    },
    {
      "id": 1,
      "text": "Capítulo 2 palavras  \\n“Não podemos mais chamar uma mulher de \\ngostosa... eu pego... você é linda... eu como  \\naquela mulher...  \\nNão podemos mais chamar um negro de negro... \\nCrioulo...  Macaco... Gorila.... Mais preto...  \\nNão podemos mais chamar o homossexual de \\nviado... Gay... Viadinho... Traveco... Ele tem  o \\npênis maior  que o meu e dá a  Bunda....  Não \\npodemos falar nada , nem para amigos?  \\nNão podemos ter forma de pensar com vício de \\nlinguagem e nos  comunicar de uma forma a qual \\neu fui criado?  \\nUma coisa é falar de uma forma avulsa e outra \\ncoisa é falarmos de uma forma de brincadeira, \\npiada, tesão, até mesmo  para uma conquista.  \\nSe falamos é ofensivo para quem escuta até que \\nponto?  \\nQual é o preconceito que mais sofre com o \\npreconceito?  \\nNão pense q ue a sua dor ou a minha dor diante \\nde sofrer preconceito é mais branda, todos o s \\ndias da minha vida eu entro em lugares que sou \\nanalisado da unha do pé até o fio de cabelo. Eu \\nentro nos lugares,  não têm quase ninguém \\nsemelhante a mim,  e quando é semelhante , está",
      "position": 10237,
      "chapter": 2,
      "page": 12,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.79108409321175,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 21,
        "paragraph_count": 1,
        "avg_sentence_length": 8.952380952380953,
        "avg_word_length": 4.382978723404255,
        "unique_word_ratio": 0.6223404255319149,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.30851063829787234,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "podemos",
          "forma",
          "chamar",
          "preconceito",
          "mulher",
          "negro",
          "falar",
          "qual",
          "coisa",
          "minha",
          "entro",
          "lugares",
          "semelhante",
          "capítulo",
          "palavras",
          "gostosa",
          "pego",
          "você",
          "linda"
        ],
        "entities": [
          [
            "2",
            "CARDINAL"
          ],
          [
            "mais chamar uma mulher de \\ngostosa",
            "PERSON"
          ],
          [
            "eu pego",
            "PERSON"
          ],
          [
            "linda",
            "PERSON"
          ],
          [
            "eu como",
            "PERSON"
          ],
          [
            "aquela mulher",
            "PERSON"
          ],
          [
            "mais chamar",
            "PERSON"
          ],
          [
            "negro de negro",
            "ORG"
          ],
          [
            "Macaco",
            "PERSON"
          ],
          [
            "Mais",
            "PERSON"
          ]
        ],
        "readability_score": 94.20891590678825,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 117,
        "lexical_diversity": 0.6223404255319149
      },
      "preservation_score": 3.555614283654386e-05
    },
    {
      "id": 1,
      "text": "trabalhando no estoque, faxina,  pedindo \\ndinheiro, cortando carne.  \\nNão p ense que o nosso sofrer preconceito é \\nmaior do que àqueles que também sofrem (todos \\nsofremos), tudo na vida é relativo e \\ninterpretativo. N ão pense que somos feitos de \\nvidro , esses que se quebram  com tudo no mundo,  \\nnão sabe o  quanto o mundo o vai destruir. Luto \\ncontra todos os preconceitos, porém luto contra \\ntodos aqueles que exageram no seu próprio \\npreconceito!  \\nPalavras são sons produzidos referentes a algo, \\nesse mesmo algo vem de uma origem do próprio \\nhumano, com peso inerente a um viver.  \\nExemplos:  \\nPreconc eito — Significado: qualquer opinião ou \\nsentimento concebido sem exame crítico. \\nSentimento hostil, assumido em consequência da \\ngeneralização apressada de uma experiência \\npessoal ou imposta pelo meio; intolerância contra \\num grupo religioso, nacional ou racial.  Etimologia: \\na palavra preconceito deriva da junção do prefixo \\npré-, que significa anterioridade, e de conceito . \\nConceito — Significado: faculdade intelectiva e \\ncognoscitiva do ser humano; mente, espírito, \\npensamento. Compreensão que alguém tem de \\numa palavra; noção, concepção, ideia . Etimologia: \\ndo latim conceptus, do verbo concipere, que",
      "position": 11407,
      "chapter": 1,
      "page": 13,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.91294466403162,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 16.727272727272727,
        "avg_word_length": 5.467391304347826,
        "unique_word_ratio": 0.7608695652173914,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.20108695652173914,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "preconceito",
          "todos",
          "contra",
          "tudo",
          "mundo",
          "luto",
          "próprio",
          "algo",
          "humano",
          "significado",
          "sentimento",
          "etimologia",
          "palavra",
          "conceito",
          "trabalhando",
          "estoque",
          "faxina",
          "pedindo",
          "dinheiro",
          "cortando"
        ],
        "entities": [
          [
            "faxina",
            "GPE"
          ],
          [
            "que também sofrem",
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
            "Palavras",
            "PERSON"
          ],
          [
            "Significado",
            "ORG"
          ],
          [
            "consequência da \\ngeneralização",
            "PERSON"
          ],
          [
            "apressada de uma",
            "PERSON"
          ],
          [
            "pelo meio",
            "PERSON"
          ],
          [
            "Etimologia",
            "GPE"
          ]
        ],
        "readability_score": 89.9961462450593,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 140,
        "lexical_diversity": 0.7608695652173914
      },
      "preservation_score": 2.7336044729925913e-05
    },
    {
      "id": 1,
      "text": "significa \\\"conter completamente\\\", \\\"formar dentro \\nde si”.  \\nO preconceito é o peso ruim de um conceito que \\nnós temos como bom ou ruim de um viver, nos \\nfazendo ter um pré-conceito  de peso, como o lado \\nbom do nosso próprio conceito.  \\nPré — Significado: A NTIGO. O pagamento diário \\nde um soldado; diária. Etimologia: origem da \\npalavra pré. Do latim prae. substantivo masculino.  \\nque se pagava diariamente; diária . \\nUniverso — Significado: o conjunto de todas as \\ncoisas que existem; o mundo,  inicial por vezes.  a \\ntotalidade dos habitantes da Terra.  Etimologia : A \\npalavra \\\"universo\\\" vem do latim \\\"universum\\\" que \\nsignifica todas as coisas, todos, o mundo todo. E \\nesta expre ssão, por sua vez, vem do adjetivo \\nlatino \\\"universus\\\", que significa \\\"tudo junto\\\"ou \\nrelativo ao todo.  \\nEnergia — Significado: capacidade que um corpo, \\numa substância ou um sistema físico têm de \\nrealizar trabalho.  Etimologia: este termo deriva \\ndo grego ergos , cujo significado original é \\nliteralmente “trabalho”. Na Física, a energia está \\nassociada à capacidade de qualquer corpo de \\nproduzir trabalho, ação ou movimento.  \\nDeus — Significado: RELIGIÃO . infinito, eterno, \\nsobrenatural e existente por si só; causa \\nnecessária e fim último de tudo que existe.",
      "position": 12748,
      "chapter": 1,
      "page": 14,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.31167557932264,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 11.647058823529411,
        "avg_word_length": 5.156565656565657,
        "unique_word_ratio": 0.7121212121212122,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.21717171717171718,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "significado",
          "significa",
          "conceito",
          "etimologia",
          "trabalho",
          "peso",
          "ruim",
          "como",
          "diária",
          "palavra",
          "latim",
          "universo",
          "todas",
          "coisas",
          "mundo",
          "todo",
          "tudo",
          "energia",
          "capacidade",
          "corpo"
        ],
        "entities": [
          [
            "significa",
            "PERSON"
          ],
          [
            "dentro \\nde si",
            "ORG"
          ],
          [
            "nós temos como",
            "ORG"
          ],
          [
            "NTIGO",
            "ORG"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "Universo",
            "GPE"
          ],
          [
            "Etimologia",
            "GPE"
          ],
          [
            "coisas",
            "NORP"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.6295008912656,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 141,
        "lexical_diversity": 0.7121212121212122
      },
      "preservation_score": 4.035320888703349e-05
    },
    {
      "id": 1,
      "text": "Etimologia: Os termos latinos deus e dīvus são \\nprovenientes do idioma protoindo -europeu \\n\\\"celestial\\\" ou \\\"brilhante\\\". Em latim clássico, deus \\n(feminino: dea) era substantivo comum,  mas \\ntecnicamente divus ou diva era u ma figura que se \\ntornara divina, como um imperador divinizado. \\nEm latino tardio, \\\"Deus\\\" veio a ser usado \\nprincipalmente para o Deus cristão. em francês  \\nDieu, espanhol  Dios, Português e Galego Deus, \\nItaliano Dio,  irlandês Dia e etc. \\nDivino — Significado: relativo a ou proveniente de \\nDeus ou de um ou mais deuses. Etimologia: \\nperfeito.  \\nSe o universo é a junção  de todos os movimentos \\ne Deus é o movimento divino . “Nós somos feitos \\ndê sua imagem e semelhança .” Tudo e todos são \\nfeitos de energia. Sem energia não há vida . Sem \\nvida não existe a morte e ambos precisam \\ncoexistir para se ter energia.  \\nVergonha — Significado: desonra que ultraja, \\nhumilha; opróbio. O sentimento desse ultraje, \\ndessa desonra ou humilhaç ão; opróbio. \\nEtimologia: cognado com vergonça, do galego -\\nportuguês medieval vergonna (“vergonha”), vindo \\nlatim verecundĭa (“descrição, vergonha”) através \\ndo acusativo verecundĭa(m).  \\nVergonha é algo que você tem perante a algo que \\nvocê pensa estar errando. Por qual motivo você \\nteria que fazer algo que lhe cause vergonha? Se",
      "position": 14120,
      "chapter": 1,
      "page": 15,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.51449067431851,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 12.058823529411764,
        "avg_word_length": 5.146341463414634,
        "unique_word_ratio": 0.7170731707317073,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.18048780487804877,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "vergonha",
          "etimologia",
          "energia",
          "algo",
          "você",
          "latim",
          "português",
          "galego",
          "divino",
          "significado",
          "todos",
          "feitos",
          "vida",
          "desonra",
          "opróbio",
          "termos",
          "latinos",
          "provenientes",
          "idioma"
        ],
        "entities": [
          [
            "dea",
            "ORG"
          ],
          [
            "tornara divina",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Dios",
            "ORG"
          ],
          [
            "Italiano Dio",
            "PERSON"
          ],
          [
            "Dia",
            "PERSON"
          ],
          [
            "perfeito",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "coexistir para se",
            "PERSON"
          ],
          [
            "opróbio",
            "PERSON"
          ]
        ],
        "readability_score": 92.42668579626972,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 147,
        "lexical_diversity": 0.7170731707317073
      },
      "preservation_score": 4.117280811174026e-05
    },
    {
      "id": 1,
      "text": "você está fazendo algo, esse algo tem uma \\nimportância, qual é a importância e por qual \\nmotivo é vergonhoso? Ter vergonha é \\nvergonhoso para si próprio.  \\nDigno — Significado: q ue merece; cre dor. Que \\nestá em conformidade; apropriado, conveniente, \\nadequado.  \\nEtimologia: que tem bom caráter; de boa \\nconduta; que demonstra dignidade: Do latim \\ndignus.a.um.  \\nDigno é o ser exemplo para si próprio. Se você \\nnão gosta que faça com você, por qual motivo \\nvocê fará com o outro? Digno é um estado de \\nviver em liberdade onde você estiver.  \\nMovimento — Significado: ou efeito de mover( -\\nse), conjunto de ações de um grupo de pessoas \\nmobilizadas por um mesmo fim. Etimologia: Veio \\ndo Latim movere, mover, fazer deslocar -se. \\nNossas vidas e tudo que existe contém \\nmovimento, a primeira forma existente de \\nenergia e a única que está em todos os tipos de \\nenergia e forças  existentes. Movimentar -se \\nequipara -se a evoluir corpo e mente.  \\nTempo — Significado: duração relativa das coi sas \\nque cria no ser humano a ideia de presente, \\npassado e futuro; período contínuo no qual os \\neventos se sucedem. Determinado período",
      "position": 15530,
      "chapter": 1,
      "page": 16,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.38962765957447,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 11.75,
        "avg_word_length": 4.840425531914893,
        "unique_word_ratio": 0.6808510638297872,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.19148936170212766,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "qual",
          "está",
          "digno",
          "significado",
          "algo",
          "importância",
          "motivo",
          "vergonhoso",
          "próprio",
          "etimologia",
          "latim",
          "movimento",
          "mover",
          "energia",
          "período",
          "fazendo",
          "esse",
          "vergonha",
          "merece"
        ],
        "entities": [
          [
            "Etimologia",
            "PERSON"
          ],
          [
            "Veio",
            "PERSON"
          ],
          [
            "Latim",
            "PERSON"
          ],
          [
            "Nossas",
            "GPE"
          ],
          [
            "Movimentar",
            "PERSON"
          ],
          [
            "Significado",
            "GPE"
          ]
        ],
        "readability_score": 92.67287234042553,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 128,
        "lexical_diversity": 0.6808510638297872
      },
      "preservation_score": 2.8203855673733093e-05
    },
    {
      "id": 1,
      "text": "considerado em relação aos acontecimentos nele \\nocorridos; época. Etimologia: a palavra tempo \\nderiva do latim tempus, oris,  fazendo referência.  \\nTempo é uma palavra igual a qualquer outra \\npalavra de marcação (peso, quilo, distância, reta ). \\nTempo existe como palavra, e não como regra. \\n“Tempo não existe”, tempo é a marcação da \\npropagação da energia.  \\nAmigo — Significado : que ama, que demonstra \\nafeto, amizade.  Em que há amizade, \\nbenevolência; amical.  \\\"conversação a. ” \\nEtimologia: Obrigado. \\\"Amigo\\\" vem do vocábulo \\nlatino \\\"amicus\\\", tendo ambas exatamente  o \\nmesmo significado. Na raiz de \\\"amicus\\\" está o \\nverbo \\\"amo\\\", que significa \\\"gostar de\\\", \\\"amar\\\".  \\nFamília — Significado: grupo de pessoas vivendo \\nsob o mesmo teto. Grupo de pessoas com \\nancestralidade comum.  Etimologia: vem do latim \\nfamulus, quer dizer escra vo doméstico, e então, \\nfamília é o conjunto dos escravos pertencentes e \\ndependentes de um chefe ou senhor. Assim era a \\nfamília greco -romana, formada por um patriarca \\ne seus famulus: esposa, filhos, servos livres e \\nescravos.  \\nEntre amigos e família, o que é mais importante?  \\nExiste amigo sem ter família?  \\nExiste família sem amizade?",
      "position": 16774,
      "chapter": 1,
      "page": 17,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.605,
      "complexity_metrics": {
        "word_count": 180,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 5.35,
        "unique_word_ratio": 0.75,
        "avg_paragraph_length": 180.0,
        "punctuation_density": 0.25555555555555554,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "família",
          "tempo",
          "palavra",
          "existe",
          "etimologia",
          "amigo",
          "significado",
          "amizade",
          "latim",
          "marcação",
          "como",
          "amicus",
          "mesmo",
          "grupo",
          "pessoas",
          "famulus",
          "escravos",
          "considerado",
          "relação",
          "acontecimentos"
        ],
        "entities": [
          [
            "aos acontecimentos nele",
            "PRODUCT"
          ],
          [
            "oris",
            "ORG"
          ],
          [
            "Tempo",
            "PRODUCT"
          ],
          [
            "benevolência",
            "PRODUCT"
          ],
          [
            "conversação a. ” \\n",
            "PERSON"
          ],
          [
            "Etimologia",
            "GPE"
          ],
          [
            "Obrigado",
            "GPE"
          ],
          [
            "Família",
            "NORP"
          ],
          [
            "Grupo de pessoas",
            "ORG"
          ],
          [
            "Etimologia",
            "GPE"
          ]
        ],
        "readability_score": 93.395,
        "semantic_density": 0,
        "word_count": 180,
        "unique_words": 135,
        "lexical_diversity": 0.75
      },
      "preservation_score": 4.1992407336447044e-05
    },
    {
      "id": 1,
      "text": "Existe amor sem amar?  \\nFracasso — Significado: som  estrepitoso \\nprovocado pela queda ou destroçamento de algo; \\nbarulho; estrondo. Falta de êxito; malogro; \\nderrota. Etimologia: do ital iano fracasso (it) \\nbaque, ruína, desgraça.  \\nTodos nós somos fracassados a partir do \\nmomento que não queremos melhorar. Nós \\nsomos fracassados com o nosso próprio medo de \\nerrar pelo julgamento de outros. O querer \\nmelhorar a vida a partir de um contexto é dign o \\nde se obter um fracasso.  \\nPalavrão — Significado: a origem dessa palavra é \\ntão esdrúxula — palavra + ão. Palavrão é o \\nextremo de algo perante o sentimento do \\nmomento. Koé viado, vai tomar no cu, você é mó \\nvacilão, fiquei te esperando e você nem \\napareceu ... Está tudo bem com você, irmão?  \\nPalavrão é a alma de se sentir livre, pois o falar o \\nfaz você fazer algo que “não deve”, é o libertar da \\nsua própria raiva ao se expressar, você fala \\npalavrão para xingar alguém, fala palavrão para \\ncumprimentar alguém, fa la palavrão para zoar \\nalguém, fala palavrão para dizer o quanto ama \\nalguém, fala palavrão quando está com raiva, fala \\npalavrão na hora do sexo, fala palavrão ao se \\nmachucar. Falar palavrão é necessário para o seu \\ndesenvolvimento em se associar -se com outro s, \\npois o falar palavrão com os outros é sinônimo de",
      "position": 18070,
      "chapter": 1,
      "page": 18,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.87466063348416,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.710407239819005,
        "unique_word_ratio": 0.6515837104072398,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.167420814479638,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "palavrão",
          "fala",
          "você",
          "alguém",
          "fracasso",
          "algo",
          "falar",
          "significado",
          "somos",
          "fracassados",
          "partir",
          "momento",
          "melhorar",
          "outros",
          "palavra",
          "está",
          "pois",
          "raiva",
          "existe",
          "amor"
        ],
        "entities": [
          [
            "sem amar",
            "PERSON"
          ],
          [
            "Fracasso",
            "GPE"
          ],
          [
            "barulho",
            "GPE"
          ],
          [
            "estrondo",
            "GPE"
          ],
          [
            "Falta de êxito",
            "ORG"
          ],
          [
            "derrota",
            "GPE"
          ],
          [
            "Etimologia",
            "PERSON"
          ],
          [
            "medo de \\n",
            "PERSON"
          ],
          [
            "pelo julgamento de outros",
            "ORG"
          ],
          [
            "você nem",
            "PERSON"
          ]
        ],
        "readability_score": 90.0868778280543,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 144,
        "lexical_diversity": 0.6515837104072398
      },
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "id": 1,
      "text": "confiança, intimidade, felicidade e tudo que você \\npode ser, com quem você pode se expressar \\nabertamente.  \\nEsses exemplos foram para demonstrar que \\ntemos palavras ruins que podemos interpretar \\ncomo boas e palavras boas que podem ser \\ninterpretadas como ruins, as palavras, ao serem \\nproferidas, já exprimem um peso, dependendo do \\nsentimento e do momento em que está \\nocorrendo a fala, dentro de um contexto, do \\nmomento ou da história vivenciada.",
      "position": 19480,
      "chapter": 1,
      "page": 19,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.09,
      "complexity_metrics": {
        "word_count": 70,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 5.3,
        "unique_word_ratio": 0.7857142857142857,
        "avg_paragraph_length": 70.0,
        "punctuation_density": 0.15714285714285714,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "palavras",
          "você",
          "pode",
          "ruins",
          "como",
          "boas",
          "momento",
          "confiança",
          "intimidade",
          "felicidade",
          "tudo",
          "quem",
          "expressar",
          "abertamente",
          "esses",
          "exemplos",
          "demonstrar",
          "temos",
          "podemos",
          "interpretar"
        ],
        "entities": [
          [
            "confiança",
            "GPE"
          ],
          [
            "quem você pode se",
            "FAC"
          ],
          [
            "boas",
            "ORG"
          ],
          [
            "serem \\nproferidas",
            "PERSON"
          ],
          [
            "já exprimem",
            "PERSON"
          ],
          [
            "da história vivenciada",
            "PERSON"
          ]
        ],
        "readability_score": 80.91,
        "semantic_density": 0,
        "word_count": 70,
        "unique_words": 55,
        "lexical_diversity": 0.7857142857142857
      },
      "preservation_score": 2.6516445505219144e-06
    },
    {
      "id": 1,
      "text": "Capítulo 3 sexo  \\nSexo é a necessidade básica mais sentimental que \\nnós temos.  \\nO sexo entre as espécies é necessário para a \\nprópria evolução, nos tornando escravos da nossa \\nprópria natureza, transformando a necessidade \\nbásica (única felicidade que tínhamos, além de \\ncomer) na maior necessidade de se viver uma \\nvida. Devido a essa luxúria, no decorrer dos anos, \\nnós começamos a acumular desejos, ganância, \\nambição, poder, posse e muitas outras derivações \\nde adaptação da espécie humana perante o \\npróprio caos gerado no mundo em que v ivemos.  \\nO sexo, com o passar do tempo, foi transformado \\nde necessidade básica para a melhor forma de se \\nviver uma vida, por efeito de nunca termos uma \\nvida de conforto, um viver com as necessidades \\nbásicas, nos transformando em escravos sexuais, \\nem consequ ência da nossa própria falta de \\nfelicidade em um viver confortável. Isso nos gerou \\numa necessidade básica dentro do nosso DNA, \\ndevido a fazer em constância para se ter \\nrelaxamento corpóreo e mental de um viver no \\n“limite” ( linha que determina uma extensão \\nespacial ou que separa duas extensões, momento, \\nespaço de tempo que determina uma duração ou \\nque separa duas durações ). \\nEssa palavra, limite, usada nesse contexto, não foi \\naplicada como eu gostaria, pois, devido a não",
      "position": 20072,
      "chapter": 3,
      "page": 20,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.004285714285714,
      "complexity_metrics": {
        "word_count": 210,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 5.014285714285714,
        "unique_word_ratio": 0.638095238095238,
        "avg_paragraph_length": 210.0,
        "punctuation_density": 0.13333333333333333,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "viver",
          "sexo",
          "básica",
          "própria",
          "vida",
          "devido",
          "escravos",
          "nossa",
          "transformando",
          "felicidade",
          "essa",
          "tempo",
          "limite",
          "determina",
          "separa",
          "duas",
          "capítulo",
          "mais",
          "sentimental"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ],
          [
            "básica",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "básica",
            "GPE"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "essa luxúria",
            "PERSON"
          ],
          [
            "derivações \\nde adaptação da espécie humana perante",
            "ORG"
          ],
          [
            "básica",
            "GPE"
          ],
          [
            "melhor forma de se",
            "PERSON"
          ],
          [
            "ência da nossa própria",
            "PERSON"
          ]
        ],
        "readability_score": 80.99571428571429,
        "semantic_density": 0,
        "word_count": 210,
        "unique_words": 134,
        "lexical_diversity": 0.638095238095238
      },
      "preservation_score": 2.2948778291789653e-05
    },
    {
      "id": 1,
      "text": "termos palavras em nosso léxico para expressar \\ndistintos sentimentos, ficamos usando aspas para \\nconfigurarmos um pensamento avulso com \\nmuitas interpretações diferentes, nos \\ntransformando em pessoas preconceituosas por \\nnão sabermos nos expressar, interpretar e \\ncompreender melhor um ao out ro. \\nOs Estados Unidos, por exemplo, têm uma \\ntendência a ter mais preconceito que no Brasil, \\ndevido à quantidade de palavras com variações \\nde sentimentos diferentes e proporcional ao \\nquerer se explicar.  \\nQuando chegamos a esse “limite”, nós \\ncomeçamos a gerar  regras (religião) para nos \\nconter perante a nossa própria necessidade, \\ngerando  regras sobre regras extremas tão \\nregradas, que a regra é digna de morte.  \\nO sexo foi direcionado através de “a minha \\nlinhagem é melhor”, através de uma percepção \\nevolutiva pera nte uma necessidade básica de \\nsobrevivência, de uma necessidade familiar ou \\nevolutiva do meio em que nós vivemos, nos \\nfazendo ter um valor hereditário do meu ser \\nmelhor que o seu ser, deixando o nosso próprio \\nser “involuído” (era para ser algo melhor, \\nentr etanto não é, devido a própria ignorância) \\npor se limitar a uma única linha de DNA, nos \\ndeixando limitados em evoluir o nosso próprio \\nDNA.",
      "position": 21481,
      "chapter": 1,
      "page": 21,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.6,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 47.25,
        "avg_word_length": 5.333333333333333,
        "unique_word_ratio": 0.6825396825396826,
        "avg_paragraph_length": 189.0,
        "punctuation_density": 0.10582010582010581,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "nosso",
          "regras",
          "necessidade",
          "palavras",
          "expressar",
          "sentimentos",
          "diferentes",
          "devido",
          "própria",
          "através",
          "evolutiva",
          "deixando",
          "próprio",
          "termos",
          "léxico",
          "distintos",
          "ficamos",
          "usando",
          "aspas"
        ],
        "entities": [
          [
            "léxico",
            "ORG"
          ],
          [
            "aspas para \\nconfigurarmos",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "querer se explicar",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "tão \\nregradas",
            "ORG"
          ],
          [
            "digna de morte",
            "PERSON"
          ],
          [
            "através de uma percepção",
            "PERSON"
          ],
          [
            "básica de \\nsobrevivência",
            "ORG"
          ],
          [
            "deixando o",
            "ORG"
          ]
        ],
        "readability_score": 74.775,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 129,
        "lexical_diversity": 0.6825396825396826
      },
      "preservation_score": 2.0248922022167342e-05
    },
    {
      "id": 1,
      "text": "Capítulo 4 religião , filosofia e matemática  \\nReligião,  filosofia e matemática são formas de \\ncaptarmos a energia do universo. Nós \\ninterpretamos essa energia como uma forma de \\nnos adaptarmos ao caos (tempo só existe  por \\ncausa das cicatrizes)  do próprio universo, do \\npróprio movimento universal, gerando ação e \\nreação constantes em prol de adaptação do \\npróprio.  \\nConforme vamos destruindo  (interferência \\nquântica) o  nosso próprio planeta, ele fica \\ninstável, doente, fora de eixo, ocasionando o \\naquecimento da Terra, derretimento das geleiras, \\naumento de nível do mar, furacões, tsunami, \\nterremo tos, erupções vulcânicas. Todos os \\neventos climáticos demonstram que o corpo da \\nterra está doente, ocasionando liberação de \\nenergia perante a sua própria doença que nós, \\nhumanos, ocasionamos. Assim, se geram formas \\nde captação de energia, mediante a nossa própria \\nadaptação do nosso próprio caos. Assim, foi a \\nnecessidade de se ter a religião,  filosofia e a \\nmatemática , pois todo o caos concentrado do \\nmundo teve uma grande evolução espiritual, \\nfilosófica, ciências, física e matemática \\nproporcional a quantidade  de caos em um \\ndeterminado espaço ocupado pelo próprio \\nhumano.",
      "position": 22826,
      "chapter": 4,
      "page": 22,
      "segment_type": "page",
      "themes": {
        "filosofia": 77.58620689655173,
        "ciencia": 22.413793103448278
      },
      "difficulty": 31.427966101694913,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 29.5,
        "avg_word_length": 5.593220338983051,
        "unique_word_ratio": 0.6892655367231638,
        "avg_paragraph_length": 177.0,
        "punctuation_density": 0.1751412429378531,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "próprio",
          "matemática",
          "energia",
          "caos",
          "religião",
          "filosofia",
          "formas",
          "universo",
          "adaptação",
          "nosso",
          "doente",
          "ocasionando",
          "terra",
          "própria",
          "assim",
          "capítulo",
          "captarmos",
          "interpretamos",
          "essa",
          "como"
        ],
        "entities": [
          [
            "4",
            "CARDINAL"
          ],
          [
            "formas de \\ncaptarmos",
            "ORG"
          ],
          [
            "uma forma de \\n",
            "PERSON"
          ],
          [
            "das cicatrizes",
            "PRODUCT"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "fora de eixo",
            "PERSON"
          ],
          [
            "terremo tos",
            "PERSON"
          ],
          [
            "erupções vulcânicas",
            "PERSON"
          ],
          [
            "ocasionando liberação de \\nenergia",
            "ORG"
          ],
          [
            "pelo próprio \\nhumano",
            "PERSON"
          ]
        ],
        "readability_score": 83.57203389830508,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 122,
        "lexical_diversity": 0.6892655367231638
      },
      "preservation_score": 2.2780037274938265e-05
    },
    {
      "id": 1,
      "text": "Com a quantidade excessiva de sexo, ganância, \\nambição, eu posso mais, eu quero mais, eu sou \\nmelhor, eu tenho direito de ter mais, começamos \\na criar mais regras (religião, filosofia, ciências, \\nmatemática), devido ao próprio mundo emitir um \\nsinal de socorro, perante a nos adaptarmos a \\nenergia universal (entrelaçamento quântico de \\nmaior estabilidade) de  contenção do caos \\nproporcional a energia do próprio universo, por \\nsermos obrigados a nos adaptar mos ao universo, \\npor questão óbvia da nossa própria sobrevivência \\nda espécie, evoluímos para os “homens \\nmodernos”, para melhor nos adaptarmos com a \\nenergia do universo (Deus, Buda, Alá e etc ). \\nQualquer forma de interpretar o bem em uma \\nescala grande de ace itação de fazer o bem é um \\npropósito de vida em escala evolutiva, porém \\nexistem as limitações de interpretação por falta \\nde entendimento ou por falta de saber se \\nexplicar, prejudicando o próprio fazer bem.",
      "position": 24145,
      "chapter": 1,
      "page": 23,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 36.5527027027027,
      "complexity_metrics": {
        "word_count": 148,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 74.0,
        "avg_word_length": 5.175675675675675,
        "unique_word_ratio": 0.6891891891891891,
        "avg_paragraph_length": 148.0,
        "punctuation_density": 0.14864864864864866,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "próprio",
          "energia",
          "universo",
          "melhor",
          "adaptarmos",
          "escala",
          "fazer",
          "falta",
          "quantidade",
          "excessiva",
          "sexo",
          "ganância",
          "ambição",
          "posso",
          "quero",
          "tenho",
          "direito",
          "começamos",
          "criar"
        ],
        "entities": [
          [
            "eu posso mais",
            "PERSON"
          ],
          [
            "eu quero mais",
            "PERSON"
          ],
          [
            "eu sou \\nmelhor",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "sobrevivência \\nda espécie",
            "PERSON"
          ],
          [
            "para melhor",
            "PERSON"
          ],
          [
            "Qualquer forma de interpretar",
            "PERSON"
          ],
          [
            "limitações de interpretação",
            "PERSON"
          ]
        ],
        "readability_score": 61.4472972972973,
        "semantic_density": 0,
        "word_count": 148,
        "unique_words": 102,
        "lexical_diversity": 0.6891891891891891
      },
      "preservation_score": 1.3740339943613556e-05
    },
    {
      "id": 1,
      "text": "Capítulo 5 apresentação do personagem  \\nComo em todo s os grandes clubes e empresas, \\ngrandes profissionais têm uma grande \\napresentação, têm um grande destaque, \\nproporcional ao seu valor monetário e \\nsentimental, nesse caso, esse cara é o que vai nos \\ndirecionar para a nossa saga preconceituosa e \\nmerece um capí tulo só para explicar por que ele \\nveio e qual é o propósito, ele está vindo para \\nagregar, evoluir conosco e também para \\npreencher as páginas do livro, para dar valor ao \\nleitor ao pagar pelo livro.  \\nVamos nos divertir, a partir de agora, com um \\nsuper -herói b em difícil de se compreender, \\nporém compreensível dentro da sua própria \\nexistência!  \\nEle é o herói mais velho que temos em toda nossa \\nexistência de “espécie racional”, ele foi gerado a \\npartir de um nada, um vácuo, um vazio, e ele \\nsurgiu através de uma simpl es forma de se gerar \\nenergia, através do movimento, pois, quando  se \\nmovimentou, surgiu o primeiro sinal de vida do \\nnosso personagem, assim surgiu a energia, ação e \\nreação, força, gravidade, luz e todos os tipos de \\nenergia se encontram no corpo d ele. \\nEle está chegando para contar a sua trajetória \\nentre aprender a falar, conversar, pedir, sentir, \\nsexo, crer em deuses, ver a evolução e a \\n“desvolução” — é a mesma origem que",
      "position": 25207,
      "chapter": 5,
      "page": 24,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.401818181818186,
      "complexity_metrics": {
        "word_count": 220,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.0,
        "avg_word_length": 4.672727272727273,
        "unique_word_ratio": 0.6727272727272727,
        "avg_paragraph_length": 220.0,
        "punctuation_density": 0.15,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "surgiu",
          "energia",
          "apresentação",
          "personagem",
          "grandes",
          "grande",
          "valor",
          "nossa",
          "está",
          "livro",
          "partir",
          "herói",
          "existência",
          "através",
          "capítulo",
          "como",
          "todo",
          "clubes",
          "empresas",
          "profissionais"
        ],
        "entities": [
          [
            "5",
            "CARDINAL"
          ],
          [
            "monetário e",
            "PERSON"
          ],
          [
            "evoluir conosco",
            "ORG"
          ],
          [
            "também para \\npreencher",
            "PERSON"
          ],
          [
            "para dar valor",
            "PERSON"
          ],
          [
            "pelo livro",
            "PERSON"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "de agora",
            "PERSON"
          ],
          [
            "herói mais velho",
            "PERSON"
          ],
          [
            "forma de se",
            "PERSON"
          ]
        ],
        "readability_score": 71.09818181818181,
        "semantic_density": 0,
        "word_count": 220,
        "unique_words": 148,
        "lexical_diversity": 0.6727272727272727
      },
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "id": 1,
      "text": "“Involutivo”, algo que evoluiu e regrediu na sua \\nprópria evolução — da própria  “desnecessidade” \\nde se ter tanta ganância evolutiva, mostrando \\ntodos os poderes de como sobreviver dentro \\ndesses 200 mil anos, senhor preconceito \\nQuântico, mais conhecido com Quântico,  é como \\nirei chamá -lo daqui em diante, no processo \\nevolutivo do nosso herói, pois escrever uma frase \\ntodas as vezes que eu for falar do senhor \\npreconceito quântico é complicado, se até o seu \\nnome não ajuda na pronúncia, tampouco \\nescrever toda hora esse nome de lorde medieval. \\nKkkkkkkk",
      "position": 26602,
      "chapter": 1,
      "page": 25,
      "segment_type": "page",
      "themes": {},
      "difficulty": 42.55393258426966,
      "complexity_metrics": {
        "word_count": 89,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 44.5,
        "avg_word_length": 5.179775280898877,
        "unique_word_ratio": 0.8426966292134831,
        "avg_paragraph_length": 89.0,
        "punctuation_density": 0.11235955056179775,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "própria",
          "como",
          "senhor",
          "preconceito",
          "escrever",
          "nome",
          "involutivo",
          "algo",
          "evoluiu",
          "regrediu",
          "evolução",
          "desnecessidade",
          "tanta",
          "ganância",
          "evolutiva",
          "mostrando",
          "todos",
          "poderes",
          "sobreviver"
        ],
        "entities": [
          [
            "da própria  “desnecessidade” \\nde se",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "preconceito \\nQuântico",
            "PERSON"
          ],
          [
            "Quântico",
            "ORG"
          ],
          [
            "irei chamá",
            "PERSON"
          ],
          [
            "nosso herói",
            "PERSON"
          ],
          [
            "preconceito",
            "PERSON"
          ],
          [
            "até o seu",
            "ORG"
          ],
          [
            "hora",
            "NORP"
          ]
        ],
        "readability_score": 76.19606741573034,
        "semantic_density": 0,
        "word_count": 89,
        "unique_words": 75,
        "lexical_diversity": 0.8426966292134831
      },
      "preservation_score": 4.62832503363825e-06
    },
    {
      "id": 1,
      "text": "Capítulo 6 o início do “homem”  \\n Quando Q uântico surgiu nós éramos... o que nós \\néramos?  \\nTínhamos um propósito de sobreviver da espécie, \\ne ele, sendo novo, não sabia nada sobre como \\nsobreviver, vivia aquilo que a necessidade o fazia \\nviver, assim ele começou a fazer coisas que nunca \\nhavia feito, po rém ele sabia que eram \\nnecessárias, pois a situação de sobrevivência dele \\nmesmo o fez evoluir durante o seu dia a dia.  \\nEm seu primeiro dia com o seu corpo, cabelo, \\nnariz, boca, pernas, braços tudo  igual ao nosso \\ncorpo , ele ficava se tocando, querendo entender \\ncomo aquele movimento  conseguiu o soltar e dar \\nvida onde só existia um vazio, como a física \\nquântica e a física do físico se juntaram e o \\nfizeram ser o que era? Durante um bom tempo \\nele ficou estagnado, interessad o de onde ele veio, \\npor qual motivo ele tem uma vida. Por qual \\nmotivo eu tenho um corpo? Por qual motivo eu \\npreciso me alimentar?  Eram tantos, que ele não \\nentendia nem o motivo de ser racional. Será que \\neu sou o escolhido? Sou o melhor de todos? Sou \\nmais f orte?  \\nSou o que eu sou, só não sei o que eu sou, \\ndescobrirei como eu vivo essa minha vida, lutarei \\npara sobreviver e fazer o melhor para viver bem.  \\nA partir desse momento, ele começou a andar \\npelo mundo procurando melhorar de vida, nessa",
      "position": 27304,
      "chapter": 6,
      "page": 26,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.38751629726206,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 18.153846153846153,
        "avg_word_length": 4.36864406779661,
        "unique_word_ratio": 0.6440677966101694,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.15677966101694915,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "vida",
          "motivo",
          "sobreviver",
          "corpo",
          "qual",
          "éramos",
          "sabia",
          "viver",
          "começou",
          "fazer",
          "eram",
          "durante",
          "onde",
          "física",
          "melhor",
          "capítulo",
          "início",
          "homem",
          "quando"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "uântico surgiu",
            "PERSON"
          ],
          [
            "sendo novo",
            "PERSON"
          ],
          [
            "nada sobre",
            "ORG"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "coisas",
            "NORP"
          ],
          [
            "havia feito",
            "PERSON"
          ],
          [
            "po rém ele sabia que",
            "PERSON"
          ],
          [
            "evoluir durante",
            "ORG"
          ],
          [
            "seu dia",
            "ORG"
          ]
        ],
        "readability_score": 89.61248370273793,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 152,
        "lexical_diversity": 0.6440677966101694
      },
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "id": 1,
      "text": "caminhada pelo mun do, percebeu que continham \\noutras espécies já existente aqui, e essas espécies \\nse alimentavam de outros animais, comiam de \\numa forma semelhante a outros animais, e esses \\noutros animais causaram um interesse peculiar, \\nele olhou para eles viu uma certa semel hança na \\naparência dele, começou a sentir algo que, até \\nentão, era desconhecido para ele, começou a \\nsentir confiança em estar com aqueles animais \\nrecém -descobertos, porém ele viu necessidade \\nem se juntar a eles para viver e não sobreviver, \\ndali em diante e le começou a interagir com \\naquela espécie que não entendia o que o \\nQuântico queria, e o Quântico, muito \\nquestionador de si mesmo, pois sentia um vazio \\npor não ter ninguém à altura, com pensamentos \\niguais ou semelhantes a ele, começou a ver a \\nnecessidade de  mostrar àquela espécie o poder \\nda comunicação, poder da organização, poder da \\nconfiança, poder de estar junto, poder de ser \\nfeliz. Após um tempo com essa espécie \\nacolhedora, Quântico começa a perceber outros \\ncostumes dessa espécie, começa a perceber que \\nessa espécie se juntava em volta de uma fogueira \\npara comer, aquecer, divertir e gerar novas crias \\npara o próprio povoado viver melhor, com mais \\nmão de obra, assim, todos conseguiam descansar, \\ndormir, fazer mais sexo e todas as outras coisas \\nnecessárias e b ásicas de se ter para um viver \\nsatisfatório.",
      "position": 28723,
      "chapter": 1,
      "page": 27,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.48938053097345,
      "complexity_metrics": {
        "word_count": 226,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 113.0,
        "avg_word_length": 4.964601769911504,
        "unique_word_ratio": 0.6150442477876106,
        "avg_paragraph_length": 226.0,
        "punctuation_density": 0.13716814159292035,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "espécie",
          "poder",
          "outros",
          "animais",
          "começou",
          "viver",
          "quântico",
          "outras",
          "espécies",
          "eles",
          "sentir",
          "confiança",
          "necessidade",
          "essa",
          "começa",
          "perceber",
          "mais",
          "caminhada",
          "pelo",
          "percebeu"
        ],
        "entities": [
          [
            "pelo mun do",
            "PERSON"
          ],
          [
            "já existente",
            "PERSON"
          ],
          [
            "de outros animais",
            "ORG"
          ],
          [
            "comiam de \\numa forma",
            "PERSON"
          ],
          [
            "outros animais",
            "PERSON"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "uma certa semel hança na \\naparência dele",
            "ORG"
          ],
          [
            "para ele",
            "PERSON"
          ],
          [
            "aquela",
            "PERSON"
          ],
          [
            "Quântico",
            "GPE"
          ]
        ],
        "readability_score": 42.01061946902655,
        "semantic_density": 0,
        "word_count": 226,
        "unique_words": 139,
        "lexical_diversity": 0.6150442477876106
      },
      "preservation_score": 2.2370237662584875e-05
    },
    {
      "id": 1,
      "text": "Capítulo 7 amor  \\nQuando conheceu o seu primeiro amor, ele se \\nsentia nas nuvens, nada o fazia ficar triste, nem \\nmesmo o caçar, pois o retorno de se ter uma \\nfelicidade quando chegar da caça era ter a \\ndiversão sexua l, o prazer era a maior \\ncompensação em se ter uma vida digna.. . \\nQuântico começou a ficar sobrecarregado, com \\nmuitas funções a desempenhar, pois, na sua área \\nde conforto, ele tinha muito trabalho a fazer e, \\ndentro do próprio povoado, observava várias \\nfamíli as com alguns filhos que ajudavam a própria \\nfamília a viver melhor, e Quântico, percebendo \\ntodas as dificuldades para caçar e fazer tudo que \\nera necessário fazer para viver melhor, viu a \\nnecessidade de ter os próprios filhos.  \\nQuântico se sentia confuso em relação a várias \\ncoisas e não sabia explicar a razão, pois ele sentia \\nalgo inexplicável perante o mundo, ele possuía \\ndesejos, sonhos, vontades, como: comer melhor, \\nfazer mais sexo, dormir agarrado mesmo no calor, \\ne isso tudo o desconcertava, pois,  aquele \\nsentimento o fazia ficar confuso, sem chão, com \\nvontade de desfrutar de mais tempo com a \\nfamília, só por gostar de estar ali. Com o passar \\ndos anos, Quântico foi entendo sobre algumas \\ncoisas daquela espécie humana ( relativo ao \\nhomem ou próprio de sua naturez a. Composto por \\nhomens. Humano é falho em ser, ser humano ), \\npercebeu que o que ele sentia não dava para",
      "position": 30217,
      "chapter": 7,
      "page": 28,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.918297872340425,
      "complexity_metrics": {
        "word_count": 235,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.166666666666664,
        "avg_word_length": 4.727659574468085,
        "unique_word_ratio": 0.6723404255319149,
        "avg_paragraph_length": 235.0,
        "punctuation_density": 0.16170212765957448,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sentia",
          "pois",
          "quântico",
          "fazer",
          "ficar",
          "melhor",
          "amor",
          "quando",
          "fazia",
          "mesmo",
          "caçar",
          "próprio",
          "várias",
          "filhos",
          "família",
          "viver",
          "tudo",
          "confuso",
          "coisas",
          "mais"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "seu primeiro amor",
            "ORG"
          ],
          [
            "nas nuvens",
            "PERSON"
          ],
          [
            "nada o",
            "ORG"
          ],
          [
            "fazia",
            "GPE"
          ],
          [
            "nem \\nmesmo",
            "PERSON"
          ],
          [
            "diversão sexua l",
            "ORG"
          ],
          [
            "Quântico",
            "ORG"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "Quântico",
            "GPE"
          ]
        ],
        "readability_score": 78.99836879432624,
        "semantic_density": 0,
        "word_count": 235,
        "unique_words": 158,
        "lexical_diversity": 0.6723404255319149
      },
      "preservation_score": 2.796279707823109e-05
    },
    {
      "id": 1,
      "text": "pagar, não dava para cicatrizar e, por muitas \\nvezes, não dava para controlar, percebeu, ainda, \\nque o sentimento dos humanos não estava no \\nconforto, estav a no bem -estar de um para com o \\noutro, notou que a felicidade do ser humano não \\nera ser apenas um humano, e sim o sentir a \\nconfiança do humano em estar um para com o \\noutro. Assim, ele descobriu o confiar, o odiar \\n(sentir aversão por algo , alguém, a si pró prio ou \\num ao outro; detestar -se, abominar -se. Achar \\nmuito desprazeroso ), admirar, entender, \\ncompreender, brigar, educar, direcionar e todos \\nos componentes necessários para se amar.",
      "position": 31710,
      "chapter": 1,
      "page": 29,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.056289308176105,
      "complexity_metrics": {
        "word_count": 106,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 35.333333333333336,
        "avg_word_length": 4.632075471698113,
        "unique_word_ratio": 0.7452830188679245,
        "avg_paragraph_length": 106.0,
        "punctuation_density": 0.22641509433962265,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "outro",
          "humano",
          "dava",
          "sentir",
          "pagar",
          "cicatrizar",
          "muitas",
          "vezes",
          "controlar",
          "percebeu",
          "ainda",
          "sentimento",
          "humanos",
          "estava",
          "conforto",
          "estav",
          "notou",
          "felicidade",
          "apenas",
          "confiança"
        ],
        "entities": [
          [
            "não dava",
            "PERSON"
          ],
          [
            "não dava",
            "ORG"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "estav",
            "PERSON"
          ],
          [
            "humano em estar",
            "ORG"
          ],
          [
            "muito desprazeroso",
            "PERSON"
          ],
          [
            "para se amar",
            "PERSON"
          ]
        ],
        "readability_score": 80.9437106918239,
        "semantic_density": 0,
        "word_count": 106,
        "unique_words": 79,
        "lexical_diversity": 0.7452830188679245
      },
      "preservation_score": 8.388839123469328e-06
    },
    {
      "id": 1,
      "text": "Capítulo 8 início da dor  \\nTudo na vida de Quântico era básico, ele tinha \\ntudo que precisava, ele estava satisfeito com a \\nvida que conquistara (vencido  pela força das \\narmas; subjugado, que foi alcançado, conseguido.  \\nPara se conquistar algo, demora uma vida; para \\nse perder uma conquista, basta um erro.). \\nQuando o nosso herói estav a feliz, com a vida \\nconcretizada, começou a perceber os problemas \\ngerados devido a um viver melhor da própria \\nespécie, pois começaram a ver a vida dele como \\nmelhor do que a minha, causando conflitos, \\ninveja, desejos, ganância, ambição e tudo que \\noutros não  conseguiam fazer por falta de \\nentender como viver o seu próprio melhor. \\nQuântico, por não entender e ver que tudo aquilo \\nque acontecia com ele e com a aldeia dele era por \\nfalta de aprendizado dos outros perante o seu \\npróprio viver, tornava -se triste, mago ado e, por \\nmuitas vezes, com vontade de sumir da sua \\nprópria aldeia com sua família, assim ele começou \\na ensinar um viver melhor para todos ali, de sua \\naldeia. Se todos conseguirem viver semelhantes à \\nminha vida, eu irei conseguir viver feliz sem \\ncausar ne nhuma indiferença, nenhuma briga, \\nnenhum problema, já que tudo que eu tenho, \\ntodos podem ter, basta cada um fazer o seu \\ntrabalho.  \\nQuântico, insatisfeito com os conflitos de sua \\naldeia, pela inveja indesejável que ele causou, o",
      "position": 32457,
      "chapter": 8,
      "page": 30,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.80451127819549,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 32.57142857142857,
        "avg_word_length": 4.824561403508772,
        "unique_word_ratio": 0.618421052631579,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "viver",
          "tudo",
          "melhor",
          "aldeia",
          "quântico",
          "todos",
          "pela",
          "basta",
          "feliz",
          "começou",
          "própria",
          "dele",
          "como",
          "minha",
          "conflitos",
          "inveja",
          "outros",
          "fazer",
          "falta"
        ],
        "entities": [
          [
            "8",
            "CARDINAL"
          ],
          [
            "vida de Quântico",
            "FAC"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "herói estav",
            "PERSON"
          ],
          [
            "desejos",
            "ORG"
          ],
          [
            "ganância",
            "PERSON"
          ],
          [
            "conseguiam fazer",
            "PERSON"
          ],
          [
            "seu próprio melhor",
            "LOC"
          ],
          [
            "Quântico",
            "PERSON"
          ]
        ],
        "readability_score": 82.26691729323309,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 141,
        "lexical_diversity": 0.618421052631579
      },
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "id": 1,
      "text": "mal estar por querer um viver  melhor para \\nQuântico e sua família... começou a ensinar a \\ntodos em sua aldeia, a se comunicar e a seguir \\nregras necessárias para não se ter brigas para \\ntodos conseguirem um viver melhor, um \\nrespeitando o outro, um ajudando o outro na \\ndificuldade em que o outro tem, porém a \\nnecessidade da outra família em não ter com \\nfacilidade o que a outra família tem em \\nabundância fez a necessidade de se aprender de \\npai para filho, pois os pais e os filhos ficavam \\njuntos o dia todo, os filhos olhavam, brincavam, \\ndormiam,  faziam quase tudo ao lado dos seus \\npais, os tornando aprendizes do trabalho da sua \\nprópria família. Quântico, por entender que a vida \\né feita de ciclos, entre erro, evolução e \\naprendizado, percebeu que todos na aldeia \\ntinham dificuldades de um viver melho r, pois \\ntudo que ele viveu com a sua família foi só ele \\nquem viveu, percebendo, assim, que não \\nadiantava ele colocar regras sobre regras para um \\nviver melhor, e sim direcionar um viver melhor. \\nQuântico, nosso herói, estava muito confuso com \\ntudo o que esta va acontecendo, pois ele estava \\nos ensinando a se comunicar, direcionar, amar, \\nrespeitar e muitas outras coisas que ele não \\nestava conseguindo assimilar, pois ele tinha a sua \\nfamília, que precisava dele por perto, precisava \\ndele para caçar, precisava dele para se aquecer, \\nprecisava dele para ter sexo e ele, por não \\nentender o que estava acontecendo com sua",
      "position": 33934,
      "chapter": 1,
      "page": 31,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.98016194331984,
      "complexity_metrics": {
        "word_count": 247,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 61.75,
        "avg_word_length": 4.724696356275303,
        "unique_word_ratio": 0.5425101214574899,
        "avg_paragraph_length": 247.0,
        "punctuation_density": 0.145748987854251,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "família",
          "viver",
          "melhor",
          "pois",
          "estava",
          "precisava",
          "dele",
          "quântico",
          "todos",
          "regras",
          "outro",
          "tudo",
          "aldeia",
          "comunicar",
          "necessidade",
          "outra",
          "pais",
          "filhos",
          "entender",
          "viveu"
        ],
        "entities": [
          [
            "mal estar",
            "PRODUCT"
          ],
          [
            "para não se",
            "PERSON"
          ],
          [
            "para \\n",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "abundância fez",
            "PERSON"
          ],
          [
            "de se aprender de \\npai para filho",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "faziam",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "foi só ele \\nquem viveu",
            "PERSON"
          ]
        ],
        "readability_score": 67.7075910931174,
        "semantic_density": 0,
        "word_count": 247,
        "unique_words": 134,
        "lexical_diversity": 0.5425101214574899
      },
      "preservation_score": 2.6034328314215155e-05
    },
    {
      "id": 1,
      "text": "aldeia, não conseguia dormir de tanta \\npreocupação, não conseguia arrumar tempo para \\nficar com os seus filhos, não conseguia tempo \\nnem para ficar com a su a fêmea. Quântico, sendo \\nfeito de energia, precisava sentir energia, \\nprecisava viver para restabelecer a sua própria \\nenergia, e tudo que estava acontecendo no seu \\nentorno não o permitia sentir a energia que era \\nnecessária para ele se sentir melhor, pois to das as \\nenergias em seu entorno o estavam fazendo \\ncanalizar de forma errada o que era necessário \\npara o seu corpo, fazendo ele ficar em dúvida \\nsobre qual energia ele devia canalizar, pois eram \\ntantas linhas de energia que passavam pelo \\nQuântico que ele se p erdeu na “ linha do próprio \\nQuântico”. Quântico, por sua vez, não era o \\nmesmo, não conseguia sentir vontade de seguir \\nadiante com a aldeia, mas ele não sabia como \\nsobreviver sem a aldeia, pois ali ele não tinha \\npredadores, não tinha tantas dificuldades em um \\nviver melhor do já viveu antes, não conseguia \\nolhar para a mulher com desejos e vontades, pois \\ntudo que ele pensava era como sobreviver \\nmelhor, não tendo tempo para pensar na mulher \\ne filhos, transformando -o em escravo do seu \\npróprio sistema.",
      "position": 35495,
      "chapter": 1,
      "page": 32,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.80544554455446,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 67.33333333333333,
        "avg_word_length": 4.797029702970297,
        "unique_word_ratio": 0.5346534653465347,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.11386138613861387,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "conseguia",
          "quântico",
          "sentir",
          "pois",
          "aldeia",
          "tempo",
          "ficar",
          "melhor",
          "filhos",
          "precisava",
          "viver",
          "tudo",
          "entorno",
          "fazendo",
          "canalizar",
          "tantas",
          "próprio",
          "como",
          "sobreviver"
        ],
        "entities": [
          [
            "nem para",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "entorno não o",
            "ORG"
          ],
          [
            "permitia",
            "ORG"
          ],
          [
            "para ele se",
            "PERSON"
          ],
          [
            "canalizar de forma errada",
            "ORG"
          ],
          [
            "necessário \\npara o seu corpo",
            "ORG"
          ],
          [
            "fazendo ele ficar em dúvida",
            "ORG"
          ],
          [
            "pelo \\nQuântico",
            "PERSON"
          ]
        ],
        "readability_score": 64.89422442244225,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 108,
        "lexical_diversity": 0.5346534653465347
      },
      "preservation_score": 1.5668808707629495e-05
    },
    {
      "id": 1,
      "text": "Capítulo 9  o tempo passa rápido  \\nQuântico, após muitas dificuldades, muito \\nesforço, muita dedicação e muito estresse, \\nconseguiu colocar regras com mais disciplina do \\nque o necessário, pois a aldeia dele teve tantos \\nconflitos desnecessários, deixando -o uma pessoa \\nmais  sábia e mais calma, devido a não ter mais \\nforça e paciência de viver uma vida em que ele \\nnão conseguia entender o motivo de viver \\ndaquela forma, fazendo ele ser mais radical com \\nas regras para conter a falta de empatia de um \\npara com o outro, criando, ass im, uma hierarquia \\n(organização fundada sobre uma ordem de \\nprioridade entre os elementos de um conjunto ou \\nsobre relações de subordinação entre os membros \\nde um grupo, com graus sucessivos de poderes, de \\nsituação e de responsabilidades. Classificação, de \\ngraduação crescente ou decrescente, segundo \\numa escala de valor, de grandeza ou de \\nimportância. ). \\nOs filhos dele cresceram, a esposa ficou mais \\nvelha, fazendo -o entender sobre o tempo da \\nenergia; como a energia do Quântico é \\nonipresente, ele não envelhece e , muito menos, \\nmorre, começou a se questionar: como aceitarei \\no meu viver?  \\nComo viverei com a dor de perder um ente \\nquerido?  \\nComo suportarei tanta dor no meu entorno?",
      "position": 36967,
      "chapter": 9,
      "page": 34,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 33.32442244224423,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 33.666666666666664,
        "avg_word_length": 4.97029702970297,
        "unique_word_ratio": 0.6435643564356436,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.1485148514851485,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "como",
          "muito",
          "viver",
          "tempo",
          "quântico",
          "regras",
          "dele",
          "entender",
          "fazendo",
          "entre",
          "energia",
          "capítulo",
          "passa",
          "rápido",
          "após",
          "muitas",
          "dificuldades",
          "esforço",
          "muita"
        ],
        "entities": [
          [
            "passa",
            "GPE"
          ],
          [
            "muito \\nesforço",
            "PERSON"
          ],
          [
            "muito estresse",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "mais calma",
            "PERSON"
          ],
          [
            "daquela forma",
            "PERSON"
          ],
          [
            "fazendo ele",
            "ORG"
          ],
          [
            "fundada",
            "PERSON"
          ],
          [
            "graus sucessivos de poderes",
            "PERSON"
          ],
          [
            "Classificação",
            "GPE"
          ]
        ],
        "readability_score": 81.67557755775577,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 130,
        "lexical_diversity": 0.6435643564356436
      },
      "preservation_score": 2.2948778291789653e-05
    },
    {
      "id": 1,
      "text": "Quântico, nesse momento de fragilidade, teve a \\nsua melhor resposta de vida, pois enxergou a \\nrazão de ser forte, corajoso e destemido, ele \\nolhou para dentro dele e se perguntou: por qual \\nmotivo você é feliz?  \\nQuantas pessoas podem viver nesse mundo?  \\nDo que adianta eu ficar triste pela perda, será que \\na minha família e as pessoas que eu a mo \\ndesejariam me ver assim?  \\nO que as pessoas que eu amo desejariam que eu \\nfizesse, pois nada eu posso fazer além do que eu \\nestou fazendo, será que eu tenho que me cobrar \\npela morte de outros?  \\nQuantas pessoas estão morrendo que não são da \\nminha família?  \\nEu estou sendo egoísta igual a todos que vivem \\nna minha aldeia, pois por qual motivo eu, minha \\nfamília e todos que eu amo merecem viver mais? \\nAté porque eu já vivo para sempre e o melhor \\nque eu posso fazer é propagar o viver melhor \\npara todos.  \\nQuântico, nesse  momento, olhou para a sua \\nfamília e para todos de sua aldeia, explicando \\naquele pensamento que veio à sua cabeça e \\npedindo conselhos. Em sua família, quase todos o \\napoiaram, menos o filho mais novo, esse filho \\nmais novo era o “mais inteligente”, queria as",
      "position": 38322,
      "chapter": 1,
      "page": 35,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 26.876960784313724,
      "complexity_metrics": {
        "word_count": 204,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.666666666666668,
        "avg_word_length": 4.426470588235294,
        "unique_word_ratio": 0.5686274509803921,
        "avg_paragraph_length": 204.0,
        "punctuation_density": 0.12745098039215685,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "família",
          "todos",
          "pessoas",
          "minha",
          "mais",
          "nesse",
          "melhor",
          "pois",
          "viver",
          "quântico",
          "momento",
          "olhou",
          "qual",
          "motivo",
          "quantas",
          "pela",
          "será",
          "desejariam",
          "posso",
          "fazer"
        ],
        "entities": [
          [
            "olhou",
            "GPE"
          ],
          [
            "para dentro dele",
            "PERSON"
          ],
          [
            "Quantas",
            "GPE"
          ],
          [
            "eu ficar",
            "PERSON"
          ],
          [
            "pela perda",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "desejariam que eu \\nfizesse",
            "PERSON"
          ],
          [
            "nada eu",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "Quantas",
            "GPE"
          ]
        ],
        "readability_score": 87.33872549019608,
        "semantic_density": 0,
        "word_count": 204,
        "unique_words": 116,
        "lexical_diversity": 0.5686274509803921
      },
      "preservation_score": 1.7549065752545035e-05
    },
    {
      "id": 1,
      "text": "melhores mulheres, as melhores comidas, as \\nmelhores camas para se dormir, o melhor lugar \\nna fogueira, tudo isso por ser filho de Quântico, \\naté porque ser filho de Quântico chama a \\natenção: ter a inteligência e a sabedoria do pai, \\nser filho do Quântico “me rece” um viver melhor, \\ntem “mais” direitos que os outros da aldeia. \\nQuântico, com sua inteligência e sabedoria sobre \\no sentir a energia, olhou para todos aqueles que \\nali estavam e disse: Para aqueles que estão contra \\na minha forma de viver, estou aqui espe rando \\numa melhor forma de viver. Quântico olhou para \\no seu filho com um olhar de amor e falou: \\nCompreendo a sua decisão, pois nem todos vão \\nconseguir enxergar o ser feliz por estar vivo, mas \\naquele que não enxerga a gratidão de se viver, \\nnão entenderá o qu e é confiança, amor, respeito, \\nadmiração e qualquer outra coisa que possa vir a \\nte fazer feliz!  \\nQuântico, no decorrer dos anos, foi evoluindo \\njunto com a aldeia, adquirindo, aprendendo com \\no comportamento e os casos do acaso (morte, \\nacidente, doença) que a conteciam. Conforme a \\naldeia ia evoluindo, a quantidade de pessoas era \\nmaior, aumentando a quantidade de comida, o \\nque gerou um aumento em retirar mais coisas do \\nplaneta Terra, desde frutas, legumes, animais, \\nágua, pedra, folhas e tudo que era necessário \\npara um viver melhor, fazendo a necessidade de \\nse criar mais regras perante o aumento de caos",
      "position": 39578,
      "chapter": 1,
      "page": 36,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.42,
      "complexity_metrics": {
        "word_count": 240,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 48.0,
        "avg_word_length": 4.733333333333333,
        "unique_word_ratio": 0.6291666666666667,
        "avg_paragraph_length": 240.0,
        "punctuation_density": 0.1625,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "viver",
          "melhor",
          "filho",
          "melhores",
          "mais",
          "aldeia",
          "tudo",
          "inteligência",
          "sabedoria",
          "olhou",
          "todos",
          "aqueles",
          "forma",
          "amor",
          "feliz",
          "evoluindo",
          "quantidade",
          "aumento",
          "mulheres"
        ],
        "entities": [
          [
            "para se dormir",
            "PERSON"
          ],
          [
            "melhor lugar",
            "GPE"
          ],
          [
            "na fogueira",
            "PERSON"
          ],
          [
            "Quântico",
            "ORG"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Quântico olhou",
            "PERSON"
          ],
          [
            "Compreendo",
            "PERSON"
          ],
          [
            "nem",
            "PERSON"
          ]
        ],
        "readability_score": 74.58,
        "semantic_density": 0,
        "word_count": 240,
        "unique_words": 151,
        "lexical_diversity": 0.6291666666666667
      },
      "preservation_score": 3.145814671300998e-05
    },
    {
      "id": 1,
      "text": "gerado pela própria adaptação, assim a aldeia \\ncomeçou a crescer ao ponto de virar tribo \\n(Divisão territorial das cidades, talvez por esta se \\nbasear, originariament e, em vínculos de \\nparentesco, grupo de pessoas com ocupações ou \\ninteresses comuns, ou ligados por laços de \\namizade. ). \\nO filho mais novo de Quântico, revoltado com o \\npai por não o entender, resolveu se rebelar \\ncontra o pai, pois a tribo estava grande, e ele  \\nqueria ser mais do que era, não bastava o ter \\ncomida, casa, fogueira e tudo aquilo que era \\nnecessário, ele queria mais que o necessário, ele \\nqueria poder viver com mais intensidade, com \\nmais ganância, ele resolveu montar a sua própria \\naldeia, com pessoas que queriam o mesmo que \\nele, que queriam “crescer e viver melhor”. Assim, \\ncomeçamos a criar aldeias que iam crescendo ao \\nponto de virar tribos.  \\nQuântico continuou a viver a sua vida do jeito que \\nprometeu para a sua primeira tribo, ensinando a \\nviver melhor dentro do que era necessário ser \\nvivido. A tribo, por viver melhor, com mais tempo \\npara fazer sexo, automaticamente aumentou a \\nquantidade de pessoas, guerreando com novas \\ntribos que iam surgindo, se adaptando à \\nquantidade de pessoas proporcional ao territó rio, \\nretirando mais recursos naturais do planeta Terra \\npara fazer ferramentas, para se proteger e para \\ncaçar com mais facilidade.",
      "position": 41099,
      "chapter": 1,
      "page": 37,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.727526395173456,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 36.833333333333336,
        "avg_word_length": 4.972850678733032,
        "unique_word_ratio": 0.5927601809954751,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "viver",
          "tribo",
          "pessoas",
          "queria",
          "necessário",
          "melhor",
          "própria",
          "assim",
          "aldeia",
          "crescer",
          "ponto",
          "virar",
          "quântico",
          "resolveu",
          "queriam",
          "tribos",
          "fazer",
          "quantidade",
          "gerado"
        ],
        "entities": [
          [
            "gerado pela",
            "PERSON"
          ],
          [
            "própria adaptação",
            "PERSON"
          ],
          [
            "Divisão",
            "ORG"
          ],
          [
            "vínculos de \\nparentesco",
            "PERSON"
          ],
          [
            "grupo de pessoas",
            "ORG"
          ],
          [
            "laços de \\namizade",
            "PERSON"
          ],
          [
            "mais novo de Quântico",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "não bastava",
            "PERSON"
          ],
          [
            "casa",
            "GPE"
          ]
        ],
        "readability_score": 80.09147812971342,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 131,
        "lexical_diversity": 0.5927601809954751
      },
      "preservation_score": 2.656465722431953e-05
    },
    {
      "id": 1,
      "text": "Capítulo 10 o início da “evolução”  \\nApós muitos anos, Quântico viu a necessidade de \\naumentar e facilitar o acesso a ter comida, devido \\nao aumento grandioso da sua tribo, Quântico \\npercebeu a forma como as plantas se \\nreproduziam, como elas cresciam, o que \\nprecisava ser feito para plantar e cultivar. Assim, \\nele começou a plantar e cultivar frutas, legumes, \\nverduras e tudo aqui lo que o planeta Terra há de \\ndar para a nossa existência.  \\nQuando Quântico percebeu que o ser humano \\nprecisava facilitar a caça, ele pensou: como posso \\nresolver esse problema?  \\nMinha tribo está crescendo, eu os amo, preciso \\nfacilitar a vida deles para facili tar a minha vida, a \\nfelicidade deles é a minha felicidade, preciso \\nconseguir chegar perto dos animais, pois vai ficar \\nmais fácil de caçá -los, como posso chegar próximo \\na eles?  \\nQuântico, o nosso herói, determinado a fazer o \\nbem, estava ficando cego perante o fazer bem, \\nmesmo com o erro de muitos da sua tribo, ele \\nficou cego diante da necessidade de evoluir \\ndevido ao nosso próprio caos. Ele olhou em seu \\nentorno e ficava lembrando das facilidades em \\nmatar certos animais. Por que matamos os \\nanimais se podemos c riar os animais?",
      "position": 42566,
      "chapter": 10,
      "page": 38,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 30.794456289978676,
      "complexity_metrics": {
        "word_count": 201,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.714285714285715,
        "avg_word_length": 4.791044776119403,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 201.0,
        "punctuation_density": 0.13930348258706468,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "como",
          "animais",
          "facilitar",
          "tribo",
          "minha",
          "muitos",
          "necessidade",
          "devido",
          "percebeu",
          "precisava",
          "plantar",
          "cultivar",
          "posso",
          "preciso",
          "vida",
          "deles",
          "felicidade",
          "chegar",
          "nosso"
        ],
        "entities": [
          [
            "Quântico",
            "ORG"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "elas cresciam",
            "PERSON"
          ],
          [
            "Quando Quântico",
            "PERSON"
          ],
          [
            "eu os amo",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "nosso herói",
            "PERSON"
          ],
          [
            "fazer",
            "ORG"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "animais se podemos",
            "PERSON"
          ]
        ],
        "readability_score": 84.20554371002132,
        "semantic_density": 0,
        "word_count": 201,
        "unique_words": 134,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 1.942932279746057e-05
    },
    {
      "id": 1,
      "text": "Quântico teve a ideia genial de domesticar os \\nanimais de fácil acesso a  matar, criando, assim, a \\nfacilidade em um viver com comida, bebida. \\nAssim, a sua tribo, por ser uma tribo bem \\nevoluída, começou a chamar a atenção pela \\nfacilidade em ter comida e essa tribo cresceu ao \\nponto de se tornar uma cidade.  \\nNo início, as cidades eram o berço da evolução \\nhumana, tinham muita comida, muitas casas, \\nsegurança em não ser morto do nada. Como \\ntodos nós já percebemos, o crescimento dos \\nhumanos é igual a uma maior retirada de recursos \\nda Terra, a retirada de recursos da Terra é igual a \\nafetar o corpo da Terra.  \\nQuântico, por sua vez, não sabia o mal que estava \\nfazendo para a própria Terra, ele não sentia o mal \\nque fazia para o próprio planeta que vivia, p ois \\nele não sentia o corpo do planeta Terra, ele sentia \\no corpo humano sofrendo, para ele, ver aquele \\nsofrimento era a maior dignidade (qualidade \\nmoral que infunde respeito; consciência do \\npróprio valor; honra, autoridade, nobreza. \\nQualidade do que é grand e, nobre, elevado. Todo \\ntrabalho que beneficia um contexto, mostra \\ndignidade para todos aqueles que foram \\nbeneficiados, porém nem todos os trabalhos que \\nlevam o peso da dignidade vêm dê uma pessoa \\ndigna. Robin Hood, Hitler, Gandhi, Karl Marx, \\nEinstein, Tes la e muitos outros foram “bons” \\ndiante de um contexto, porém todos foram bons",
      "position": 43876,
      "chapter": 1,
      "page": 39,
      "segment_type": "page",
      "themes": {
        "filosofia": 69.76744186046511,
        "ciencia": 30.232558139534888
      },
      "difficulty": 31.101968085106382,
      "complexity_metrics": {
        "word_count": 235,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 29.375,
        "avg_word_length": 4.714893617021277,
        "unique_word_ratio": 0.6425531914893617,
        "avg_paragraph_length": 235.0,
        "punctuation_density": 0.17446808510638298,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "terra",
          "todos",
          "comida",
          "tribo",
          "corpo",
          "sentia",
          "dignidade",
          "quântico",
          "assim",
          "facilidade",
          "igual",
          "maior",
          "retirada",
          "recursos",
          "próprio",
          "planeta",
          "qualidade",
          "contexto",
          "porém",
          "bons"
        ],
        "entities": [
          [
            "Assim",
            "ORG"
          ],
          [
            "de se tornar uma cidade",
            "PERSON"
          ],
          [
            "berço da evolução \\nhumana",
            "ORG"
          ],
          [
            "tinham muita",
            "PERSON"
          ],
          [
            "casas",
            "GPE"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "já percebemos",
            "PERSON"
          ],
          [
            "por sua vez",
            "ORG"
          ],
          [
            "fazendo",
            "ORG"
          ]
        ],
        "readability_score": 83.89803191489362,
        "semantic_density": 0,
        "word_count": 235,
        "unique_words": 151,
        "lexical_diversity": 0.6425531914893617
      },
      "preservation_score": 3.07590767860542e-05
    },
    {
      "id": 1,
      "text": "em sua vida?), mal sabia ele que o seu excesso de \\ndignidade o deixava cego em ser digno com o \\nplaneta Terra, pois, assim como ele sentia a \\nenergia do humano, ele sentia a energia  da Terra, \\nmas ele estava tão cego perante a sentir a \\nenergia, devido ao apego pelo sentimento criado \\npelos humanos, que ele não tinha entendido o \\nverdadeiro motivo de estar aqui no planeta Terra.  \\nQuântico começou a dar ênfase em sentir a \\nenergia do planet a Terra, percebeu que o que ele \\ntinha feito de benéfico para o humano era \\nprejuízo para o motivo de ele ter sido criado, ele \\nperdeu a conexão com a maior energia próxima \\ndele, ele ficou cego diante da sua própria \\ndignidade e percebeu que os seus erros já n ão \\ntinham mais conserto, pois o planeta Terra estava \\ntão doente, tão danificado, que ele começou a \\npedir “socorro” para os seres que ali estavam \\nhabitando, o caos no mundo devido a expansão \\ndo próprio humano fez o ser humano sentir a \\nenergia de socorro do próprio mundo. Quântico, \\ndesesperado, sem saber o que fazer, desistiu de \\nviver junto com os humanos e começou a se \\npropagar como energia na mente dos humanos \\npara tentar conter o próprio caos gerado por ele.",
      "position": 45366,
      "chapter": 2,
      "page": 40,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.48679245283019,
      "complexity_metrics": {
        "word_count": 212,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 53.0,
        "avg_word_length": 4.452830188679245,
        "unique_word_ratio": 0.5660377358490566,
        "avg_paragraph_length": 212.0,
        "punctuation_density": 0.09905660377358491,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "terra",
          "humano",
          "cego",
          "planeta",
          "sentir",
          "humanos",
          "começou",
          "próprio",
          "dignidade",
          "pois",
          "como",
          "sentia",
          "estava",
          "devido",
          "criado",
          "tinha",
          "motivo",
          "quântico",
          "percebeu"
        ],
        "entities": [
          [
            "mal sabia ele que",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "excesso de \\ndignidade",
            "PERSON"
          ],
          [
            "deixava cego",
            "PERSON"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "mas ele estava",
            "PERSON"
          ],
          [
            "apego pelo",
            "PERSON"
          ],
          [
            "criado \\npelos humanos",
            "PERSON"
          ],
          [
            "verdadeiro motivo de estar",
            "ORG"
          ],
          [
            "Terra",
            "PERSON"
          ]
        ],
        "readability_score": 72.16415094339622,
        "semantic_density": 0,
        "word_count": 212,
        "unique_words": 120,
        "lexical_diversity": 0.5660377358490566
      },
      "preservation_score": 1.388497510091475e-05
    },
    {
      "id": 1,
      "text": "Capítulo 11 será que vai dar certo?  \\nO caos no mu ndo estava generalizado, as cidades \\nviraram metrópoles cheias de ganância (â nsia por \\nganhos exorbitantes; avidez, cobiça, cupidez. \\nDesejo exacerbado de ter ou de receber mais do \\nque os outros. ), cheias de destruição, desejo de \\nser mais, eu posso ser mais, eu quero ser mais. “É \\ntanto egocentrismo que não temos palavras para \\nproporcionar o tamanho”, gerando uma “doença” \\nmaior na Terra, proporcional a região afetada do \\npróprio planeta Terra, assim criando um pedido \\nde socorro do planeta perante a necessidade d o \\npróprio humano em sobreviver junto a ele, pela \\nnecessidade de sobrevivência do próprio ser \\nhumano de captar a energia do planeta Terra. \\nVoltamos com o senhor preconceito Quântico, \\naté porque ele, até agora, só se fodeu , será que \\nem algum momento vai cons eguir ser feliz? Creio \\nque sim, pois até um leão consegue ser feliz \\ndepois de tanta luta, para ele fazer sexo tem que \\nganhar do leão mais forte e para comer, tem que \\ncaçar, depois de conseguir isso, nota -se como ele \\ndorme feliz.  \\nO Quântico se juntou à ener gia do universo, ele \\nresolveu plantar ideias na cabeça do ser, acerca \\nde interpretação, sobre um viver com o planeta \\nTerra em harmonia. O Quântico percebeu que, \\napós ele perder o controle, não podia deixar de \\nreparar a merda  que ele fez, a sua existência é  \\nenergia, fazer dele a melhor energia é a maior",
      "position": 46824,
      "chapter": 11,
      "page": 42,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 31.95719489981785,
      "complexity_metrics": {
        "word_count": 244,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 27.11111111111111,
        "avg_word_length": 4.672131147540983,
        "unique_word_ratio": 0.6639344262295082,
        "avg_paragraph_length": 244.0,
        "punctuation_density": 0.14754098360655737,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "terra",
          "planeta",
          "próprio",
          "energia",
          "quântico",
          "feliz",
          "será",
          "cheias",
          "desejo",
          "maior",
          "necessidade",
          "humano",
          "leão",
          "depois",
          "fazer",
          "capítulo",
          "certo",
          "caos",
          "estava"
        ],
        "entities": [
          [
            "estava generalizado",
            "PERSON"
          ],
          [
            "avidez",
            "ORG"
          ],
          [
            "Desejo",
            "PERSON"
          ],
          [
            "desejo de \\nser mais",
            "PERSON"
          ],
          [
            "eu posso",
            "PERSON"
          ],
          [
            "eu quero",
            "PERSON"
          ],
          [
            "ser mais",
            "PERSON"
          ],
          [
            "palavras",
            "NORP"
          ],
          [
            "para \\nproporcionar",
            "PERSON"
          ],
          [
            "Terra",
            "ORG"
          ]
        ],
        "readability_score": 85.04280510018215,
        "semantic_density": 0,
        "word_count": 244,
        "unique_words": 162,
        "lexical_diversity": 0.6639344262295082
      },
      "preservation_score": 3.0060006859098423e-05
    },
    {
      "id": 1,
      "text": "conquista dele, Quântico estava determinado a \\nreparar o próprio erro, foi quando pensou: \\ncolocarei as ideias em pessoas, que conseguem \\nme ouvir e interpretar melhor dentro do caos que \\nvivo. Quântico começou a  analisar que o mundo \\ncresceu muito mais do que ele esperava, pois \\ncada parte do planeta Terra continha muito caos, \\nas grandes metrópoles não conseguiam se \\ncontrolar no próprio crescimento, fazendo grande \\ncaos na região do planeta Terra, proporcional à \\nárea habitada, assim o Quântico começou a \\nentender a energia do planeta Terra junto aos \\nhumanos.  \\nQuântico olhou para a Palestina e falou: ali a \\nsituação está braba demais, como resolverei esse \\nproblema?  Quântico lançou um  eureka !!! \\nMostrarei a eles a energia do universo em forma \\nde Deus, pois, se eles sentirem a energia do \\nuniverso, não haverá energia que possa destruir. \\nO humano consegue burlar qualquer sistema de \\ncontrole, por mais que eu mostre a eles a \\nresposta que precisam diante dos próprios erros, \\neles não querem enxergar a sua própria \\ndestruição.  \\n Na Índia (lumbini, Nepal), Quântico estava \\nolhando para eles e pensou: vou fazer diferente \\nnesse local aqui, a galera daqui parece ser menos \\nagressiva, vou falar para eles não fazerem mal a \\nnenhum ser vivo, po is eles entenderão que o viver \\ncom o necessário devido a grande quantidade de",
      "position": 48356,
      "chapter": 2,
      "page": 43,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 33.94101382488479,
      "complexity_metrics": {
        "word_count": 217,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 31.0,
        "avg_word_length": 5.04147465437788,
        "unique_word_ratio": 0.6774193548387096,
        "avg_paragraph_length": 217.0,
        "punctuation_density": 0.1382488479262673,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "eles",
          "quântico",
          "energia",
          "caos",
          "planeta",
          "terra",
          "estava",
          "próprio",
          "pensou",
          "vivo",
          "começou",
          "muito",
          "mais",
          "pois",
          "grande",
          "universo",
          "conquista",
          "dele",
          "determinado",
          "reparar"
        ],
        "entities": [
          [
            "conquista dele",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "foi quando",
            "PERSON"
          ],
          [
            "Quântico",
            "ORG"
          ],
          [
            "muito mais",
            "PERSON"
          ],
          [
            "que ele esperava",
            "PERSON"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "área habitada",
            "PERSON"
          ],
          [
            "Quântico",
            "ORG"
          ]
        ],
        "readability_score": 82.98755760368664,
        "semantic_density": 0,
        "word_count": 217,
        "unique_words": 147,
        "lexical_diversity": 0.6774193548387096
      },
      "preservation_score": 2.2370237662584875e-05
    },
    {
      "id": 1,
      "text": "humanos  que ali habitavam, será o suficiente \\npara se manter em harmonia com todos os seres \\nvivos, fazendo todo mundo ter uma vida plena e \\nsaudável.  \\nAqui, na Grécia, a galera gost a de luxo, sexo, \\ndecoração, estudar, aqui vou fazer a galera \\npensar um pouco, vou diminuir o caos deles com a \\nfilosofia, ciências e outras coisas de maluco que \\ntalvez ninguém entenda, até porque “só sei o que \\nnada sei”, vai que eles entendem essa parada e \\nme falam o que eles sabem.  \\nQuântico pensou assim: agora vai dar certo, fui \\naté as pessoas certas para propagar a mensagem \\nque vai dar merda o que eles estão fazendo; dessa \\nvez, eu tenho fé na raça humana, pois, se não der \\ncerto, o planeta Terra vai destrui r uma parte \\ndeles, e eu não conseguirei fazer nada!",
      "position": 49817,
      "chapter": 2,
      "page": 44,
      "segment_type": "page",
      "themes": {
        "filosofia": 39.473684210526315,
        "ciencia": 34.21052631578947,
        "arte": 26.31578947368421
      },
      "difficulty": 36.31739130434782,
      "complexity_metrics": {
        "word_count": 138,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 46.0,
        "avg_word_length": 4.391304347826087,
        "unique_word_ratio": 0.7318840579710145,
        "avg_paragraph_length": 138.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 16,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "eles",
          "fazendo",
          "aqui",
          "galera",
          "fazer",
          "deles",
          "nada",
          "certo",
          "humanos",
          "habitavam",
          "será",
          "suficiente",
          "manter",
          "harmonia",
          "todos",
          "seres",
          "vivos",
          "todo",
          "mundo",
          "vida"
        ],
        "entities": [
          [
            "para se manter",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Grécia",
            "PERSON"
          ],
          [
            "aqui vou",
            "PERSON"
          ],
          [
            "vou diminuir",
            "PERSON"
          ],
          [
            "coisas de maluco",
            "PERSON"
          ],
          [
            "talvez ninguém entenda",
            "PERSON"
          ],
          [
            "entendem essa parada e",
            "ORG"
          ],
          [
            "falam",
            "GPE"
          ],
          [
            "Quântico",
            "PERSON"
          ]
        ],
        "readability_score": 75.68260869565218,
        "semantic_density": 0,
        "word_count": 138,
        "unique_words": 101,
        "lexical_diversity": 0.7318840579710145
      },
      "preservation_score": 9.642343820079688e-06
    },
    {
      "id": 1,
      "text": "Capítulo 12 “generalizar o generalizado”  \\nQuântico plantou umas ideias iniciais na mente \\ndas pessoas, essas pessoas começaram a \\npropagar a ideia de Quântico, um falava sobre \\nZeus; o outro, sobre viver em h armonia e vários \\noutros falavam de várias formas diferentes de \\ncomo direcionar -se para o bem. Desde pajé, \\nmago, uns com mais intensidade devido ao caos \\nregional, outros com menos importância, que até \\nse perderam na história, e lá estava o Quântico \\nfazendo todos se organizarem na própria \\nbagunça, muito esforço para todos acreditarem \\nna mensagem de necessidade para eles mesmos, \\naté que começaram a acreditar nos deuses do \\ntrovão, floresta, chuva, saci, ET de Varginha, o \\nque for melhorar um viver está ótimo. A ideia \\ndele foi tão boa, tão boa que deu merda  de novo, \\ndevido a própria interpretação do humano em ter \\nganância, pois, mais uma vez, o humano usou \\nDeus, Buda, Alá, Odin, Zeus para o seu próprio \\nbenefício, todas as regras impostas para conter a \\npropagação d o caos foram distorcidas, \\nmanipuladas, controladas de uma forma \\nestratégica para o próprio benefício.  \\nCom as regras religiosas e filosóficas impostas \\npara uma forma de um viver melhor, criamos o \\nexagero das próprias regras, pois a mesma regra \\nque beneficia, gera benefícios maiores para \\noutros que sabem interpretar de uma forma \\ngananciosa aquele benefício.",
      "position": 50866,
      "chapter": 12,
      "page": 46,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.52602739726028,
      "complexity_metrics": {
        "word_count": 219,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 54.75,
        "avg_word_length": 5.0867579908675795,
        "unique_word_ratio": 0.6712328767123288,
        "avg_paragraph_length": 219.0,
        "punctuation_density": 0.1598173515981735,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "viver",
          "outros",
          "benefício",
          "regras",
          "forma",
          "pessoas",
          "começaram",
          "ideia",
          "zeus",
          "mais",
          "devido",
          "caos",
          "todos",
          "própria",
          "humano",
          "pois",
          "próprio",
          "impostas",
          "capítulo"
        ],
        "entities": [
          [
            "12",
            "CARDINAL"
          ],
          [
            "de Quântico",
            "PERSON"
          ],
          [
            "Zeus",
            "PERSON"
          ],
          [
            "outros falavam de várias",
            "PERSON"
          ],
          [
            "estava",
            "PERSON"
          ],
          [
            "se organizarem na própria \\nbagunça",
            "PERSON"
          ],
          [
            "muito esforço",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "floresta",
            "ORG"
          ]
        ],
        "readability_score": 71.09897260273972,
        "semantic_density": 0,
        "word_count": 219,
        "unique_words": 147,
        "lexical_diversity": 0.6712328767123288
      },
      "preservation_score": 2.656465722431953e-05
    },
    {
      "id": 1,
      "text": "Devido ao crescimento para metrópoles, nós \\ncomeçamos a ter a necessidade de desenvolver \\numa forma de se ganhar devido ao trabalho, \\ngeramos o sist ema de trocas humanas, animais, \\nprodutos, frutas e tudo necessário para \\nsobreviver de acordo com a tecnologia do tempo. \\nApós um tempo, essa forma de pagamento, \\ndevido à dificuldade, foi sendo trocada pelas \\nmoedas.  \\nSexo estava um Sodoma e Gomorra, uma Vila \\nMimosa elevada a 100, um Deus nos acuda. \\nEstávamos sem controle de natalidade nenhum, \\ntodo mundo transava com todo mundo, pois nós \\néramos animais com vontades e desejos sem ter \\ncio, imagina como era, pensa comigo, nós não \\ntínhamos televisão, não tínhamos n ada para \\nfazer, não tínhamos camisinha, o que você ia \\nfazer não tendo nada para fazer? Por isso, quando \\nolhamos para os livros de história, as famílias \\nantigas são formadas por 30 filhos, 20 filhos... \\nComo você controlaria o desejo de um humano?  \\nForam cria das as regras para se conter o próprio \\ncrescimento, pois o fazer regras para conter o \\nmeu desejo sexual é necessário para se ter um \\ncontrole populacional e estrutural de um \\ncontexto. Assim, começamos as proibições \\nsexuais: ter um homem para uma mulher, não  \\ncobiçar a mulher do próximo, grandes líderes \\nreligiosos não poderem ter filhos para não cair na",
      "position": 52347,
      "chapter": 2,
      "page": 47,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 31.85397196261682,
      "complexity_metrics": {
        "word_count": 214,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 26.75,
        "avg_word_length": 4.929906542056075,
        "unique_word_ratio": 0.6635514018691588,
        "avg_paragraph_length": 214.0,
        "punctuation_density": 0.16355140186915887,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "devido",
          "tínhamos",
          "filhos",
          "crescimento",
          "começamos",
          "forma",
          "animais",
          "necessário",
          "tempo",
          "controle",
          "todo",
          "mundo",
          "pois",
          "como",
          "você",
          "desejo",
          "regras",
          "conter",
          "mulher"
        ],
        "entities": [
          [
            "Devido",
            "PERSON"
          ],
          [
            "ganhar devido",
            "PERSON"
          ],
          [
            "ema de trocas humanas",
            "PERSON"
          ],
          [
            "animais",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "sobreviver de acordo",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "essa forma de pagamento",
            "PERSON"
          ],
          [
            "trocada pelas \\nmoedas",
            "PERSON"
          ],
          [
            "Sodoma e Gomorra",
            "ORG"
          ]
        ],
        "readability_score": 85.14602803738318,
        "semantic_density": 0,
        "word_count": 214,
        "unique_words": 142,
        "lexical_diversity": 0.6635514018691588
      },
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "id": 1,
      "text": "tentação e deixar de ser exemplo e muitas outras \\nque eu não tenho a menor ideia.",
      "position": 53762,
      "chapter": 2,
      "page": 48,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.21875,
      "complexity_metrics": {
        "word_count": 16,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 16.0,
        "avg_word_length": 4.0625,
        "unique_word_ratio": 0.9375,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.0625,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tentação",
          "deixar",
          "exemplo",
          "muitas",
          "outras",
          "tenho",
          "menor",
          "ideia"
        ],
        "entities": [
          [
            "deixar de ser",
            "PERSON"
          ],
          [
            "que eu não",
            "PERSON"
          ]
        ],
        "readability_score": 90.78125,
        "semantic_density": 0,
        "word_count": 16,
        "unique_words": 15,
        "lexical_diversity": 0.9375
      },
      "preservation_score": 2.410585955019922e-08
    },
    {
      "id": 1,
      "text": "Capítulo 13 deu merda  \\nO tiro do Quântico para conter o caos deu ruim , \\npois, através das regras religiosas, geramos \\nmuitos preconceitos e, dentro desses \\npreconceitos, vieram muitos outros: em não ser \\nde determinada religião, de não seguir a conduta \\nreligiosa, de julgarmos um ao outro e muitos \\noutros que provavelmente falarei no decorrer do \\nlivro.  \\nAtravés da religião, conseguimos aumentar a \\nquantidade de escravos para a nossa própria \\nganância, aumentamos a quantidade de mão de \\nobra barata, assim aumentamos a produtividade \\nda nossa  ganância, criamos estruturas em nomes \\nde deuses, criamos templos, criamos mais luxo, \\ncriamos tanto defeitos que não conseguimos \\ncontrolar o viver melhor, em uma escada de \\nproporção infinita de sempre ser melhor que o \\nmelhor.  \\nNesse momento da história, Quâ ntico tentava \\ncontrolar tudo o que acontecia, e não estava \\nconseguindo, pois em uma frente estava a \\nPalestina, cheia de escravos com profetas e \\nmessias comandando a loucura que ali estava \\nacontecendo, em outra frente estava a Grécia em \\nguerra política e ci vil, na outra frente estava a \\nguerra no continente asiático. Quântico se \\nencontrava desesperado, pois o planeta Terra \\nestava exalando socorro para todos os lados, e",
      "position": 54150,
      "chapter": 13,
      "page": 50,
      "segment_type": "page",
      "themes": {},
      "difficulty": 42.577319587628864,
      "complexity_metrics": {
        "word_count": 194,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 48.5,
        "avg_word_length": 5.257731958762887,
        "unique_word_ratio": 0.6391752577319587,
        "avg_paragraph_length": 194.0,
        "punctuation_density": 0.13917525773195877,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estava",
          "criamos",
          "pois",
          "muitos",
          "melhor",
          "frente",
          "quântico",
          "através",
          "preconceitos",
          "outros",
          "religião",
          "conseguimos",
          "quantidade",
          "escravos",
          "nossa",
          "ganância",
          "aumentamos",
          "controlar",
          "outra",
          "guerra"
        ],
        "entities": [
          [
            "13",
            "CARDINAL"
          ],
          [
            "Quântico",
            "GPE"
          ],
          [
            "aumentamos",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "da história",
            "PERSON"
          ],
          [
            "Quâ ntico",
            "PERSON"
          ],
          [
            "frente estava",
            "PERSON"
          ],
          [
            "cheia de escravos",
            "PERSON"
          ],
          [
            "ali estava \\nacontecendo",
            "PERSON"
          ],
          [
            "frente estava",
            "PERSON"
          ]
        ],
        "readability_score": 74.17268041237114,
        "semantic_density": 0,
        "word_count": 194,
        "unique_words": 124,
        "lexical_diversity": 0.6391752577319587
      },
      "preservation_score": 1.822402981995061e-05
    },
    {
      "id": 1,
      "text": "nós estávamos destruindo cada vez mais o corpo \\ndo planeta Terra e, cada vez mais, ela pedia  \\nsocorro, socorro, socorro!  \\nE nós humanos estávamos “felizes da vida”, várias \\ncaptações de energia para se controlar e nós só \\nevoluímos com o nosso próprio caos, criamos \\narmas mais avançadas, criamos uma doutrina \\nmelhor para o nosso próprio benefício, cria mos \\nremédios, criamos casas melhores e tudo que foi \\ncriado, foi  devido ao nosso próprio caos para nos \\nadaptarmos a ele. As regras estavam sendo mais \\nvalorizadas que a própria vida humana, pois as \\nregras eram para ser tão seguidas que, se não \\nfossem seguida s, você era condenado a morte.  \\nApós todos os problemas, o Quântico não teve \\nmais o que fazer, pois todas as tentativas dele \\nforam frustradas. Depois de sua desistência, as \\ncoisas ficaram piores para o humano, pois aí veio \\na merda  que o mundo estava anuncia ndo, o pior \\nperíodo para se viver na Terra veio com um \\ngrande cataclismo de um vulcão e, logo após esse \\ncataclismo, veio a idade média e, junto com ela, \\nas guerras por luxúria do próprio humano, pois o \\nQuântico havia desaparecido, a energia do \\nplaneta Terr a estava se restaurando, os humanos \\nvivendo em guerra devido a não ter direção, não \\nsabiam o que fazer. Em meio às cruzadas, não \\npossuíam escravos suficientes, aí arrumaram uma \\nideia que não poderia ser pior: falaram que o filho \\nde Noé, Cam e todos os seus  filhos, e filho dos",
      "position": 55512,
      "chapter": 2,
      "page": 51,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.40243902439025,
      "complexity_metrics": {
        "word_count": 246,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.0,
        "avg_word_length": 4.67479674796748,
        "unique_word_ratio": 0.6341463414634146,
        "avg_paragraph_length": 246.0,
        "punctuation_density": 0.14634146341463414,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "próprio",
          "pois",
          "socorro",
          "nosso",
          "criamos",
          "veio",
          "estávamos",
          "cada",
          "planeta",
          "terra",
          "humanos",
          "vida",
          "energia",
          "caos",
          "devido",
          "regras",
          "após",
          "todos",
          "quântico"
        ],
        "entities": [
          [
            "nós estávamos",
            "GPE"
          ],
          [
            "destruindo",
            "ORG"
          ],
          [
            "cada vez mais",
            "ORG"
          ],
          [
            "cada vez mais",
            "ORG"
          ],
          [
            "ela pedia  \\n",
            "PERSON"
          ],
          [
            "para se controlar",
            "PERSON"
          ],
          [
            "armas mais avançadas",
            "WORK_OF_ART"
          ],
          [
            "cria mos",
            "PERSON"
          ],
          [
            "vida humana",
            "PERSON"
          ],
          [
            "ser tão seguidas que",
            "ORG"
          ]
        ],
        "readability_score": 78.09756097560975,
        "semantic_density": 0,
        "word_count": 246,
        "unique_words": 156,
        "lexical_diversity": 0.6341463414634146
      },
      "preservation_score": 2.656465722431953e-05
    },
    {
      "id": 1,
      "text": "filhos, assim eternamente, não entrariam no \\nreino do céu, todos eles são condenados a serem \\nservos dos servos a seus irmãos. Assim, foi criada \\na escravidão dos negros.",
      "position": 57058,
      "chapter": 2,
      "page": 52,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.5,
      "complexity_metrics": {
        "word_count": 28,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 14.0,
        "avg_word_length": 5.0,
        "unique_word_ratio": 0.8571428571428571,
        "avg_paragraph_length": 28.0,
        "punctuation_density": 0.21428571428571427,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "servos",
          "filhos",
          "eternamente",
          "entrariam",
          "reino",
          "todos",
          "eles",
          "condenados",
          "serem",
          "seus",
          "irmãos",
          "criada",
          "escravidão",
          "negros"
        ],
        "entities": [
          [
            "filhos",
            "ORG"
          ],
          [
            "não entrariam",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "servos",
            "GPE"
          ],
          [
            "servos",
            "GPE"
          ]
        ],
        "readability_score": 91.5,
        "semantic_density": 0,
        "word_count": 28,
        "unique_words": 24,
        "lexical_diversity": 0.8571428571428571
      },
      "preservation_score": 4.3390547190358593e-07
    },
    {
      "id": 1,
      "text": "Capítulo 14 a volta do que não foi  \\nQuântico, triste com tudo que ve io a acontecer \\ndurante todo o período em que ele tomou \\nconhecimento da raça humana , percebeu que \\nnão tinha muito o que fazer, voltou a edificar a \\nraça humana e começou a plantar ideias, a fazer o \\nser humano evoluir para se ter mais conforto, \\nigual quando Quântico surgiu no mundo, não \\nprecisávamos fazer muitas coisas, porém as \\npoucas coisas que nós fazíamos eram necessárias \\npara se viver, Quântico teve a ideia genial de \\nfocar na área da tecnologia, ciências, filosofia, \\nmatemática, evolução, adaptação perant e o \\npróprio desenvolvimento, pois ele viu que, na \\nGrécia, o desenvolvimento cultural e social foi \\numa evolução menos agressiva que a religião,  \\nassim, ele resolveu fazer a sua própria energia ser \\ncaptada, ensinando a todos o quão difícil é \\ninterpretar o “só sei que nada sei” , dessa maneira \\nele fez os humanos evoluírem a tecnologia \\nperante o seu próprio caos, com uma consistência \\nmaior após o planeta Terra se reorganizar e a \\nenergia do Quântico ser sentida de novo, pois a \\nausência de energia do planeta Terra  não deixava \\no Quântico se movimentar entre as linhas de \\nenergia que pairam o nosso planeta, devido a \\nmassa escura estar muito mais densa, assim foi \\ndiminuindo os caminhos quânticos que ele fazia \\ncom frequência.",
      "position": 57533,
      "chapter": 14,
      "page": 54,
      "segment_type": "page",
      "themes": {
        "filosofia": 20.27027027027027,
        "ciencia": 52.70270270270271,
        "tecnologia": 27.027027027027025
      },
      "difficulty": 36.44776785714286,
      "complexity_metrics": {
        "word_count": 224,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 224.0,
        "avg_word_length": 4.825892857142857,
        "unique_word_ratio": 0.6473214285714286,
        "avg_paragraph_length": 224.0,
        "punctuation_density": 0.11160714285714286,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "fazer",
          "energia",
          "planeta",
          "raça",
          "humana",
          "muito",
          "mais",
          "coisas",
          "tecnologia",
          "evolução",
          "próprio",
          "desenvolvimento",
          "pois",
          "assim",
          "terra",
          "capítulo",
          "volta",
          "triste",
          "tudo"
        ],
        "entities": [
          [
            "da raça humana",
            "PERSON"
          ],
          [
            "humano evoluir",
            "PERSON"
          ],
          [
            "Quântico surgiu",
            "PERSON"
          ],
          [
            "muitas coisas",
            "PERSON"
          ],
          [
            "para se viver",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "Grécia",
            "PERSON"
          ],
          [
            "sua própria",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "dessa maneira \\nele fez",
            "PERSON"
          ]
        ],
        "readability_score": 0,
        "semantic_density": 0,
        "word_count": 224,
        "unique_words": 145,
        "lexical_diversity": 0.6473214285714286
      },
      "preservation_score": 1.822402981995061e-05
    },
    {
      "id": 1,
      "text": "Quântico, mais determinado que o Joseph \\nClim ber, após muitos esforços, muito gasto de \\nenergia para conter o próprio excesso, Quântico \\nseguiu uma regra de evoluir o amor, evoluir a \\nmatemática, evoluir a espécie humana para \\ntrabalhar menos e ter tempo para não fazer nada, \\npois, assim, eles não destrui riam novamente o \\nplaneta Terra, pois já viram o que aconteceu, \\ncontinuariam? Creio que, com todos os \\nensinamentos que eu passei, eles entenderam e \\nsaberão usar para um propósito maior de viver \\nem harmonia com o planeta Terra, deixarei a \\nreligião se propaga r da forma que tem que ser, \\nassim a sabedoria de interpretar a energia irá \\nguiar todos para a mesma direção, seja ela \\nreligiosa, estudiosos, matemáticos, filosóficos e \\ntudo aquilo que possa fazer o bem, como uma \\nforma de melhorar o planeta Terra, para todo s \\nnós sentirmos, nos conectarmos e vivermos em \\numa harmonia constante um para com todos!  \\nQuântico começou a implementar a evolução da \\nfilosofia, no intuito de mostrar com mais \\ninsistência a matemática da energia para facilitar \\no direcionamento da mesma. Qu ântico começou \\na mostrar aos humanos o conhecimento de \\ninterpretar o passado através da matemática, \\nvem mostrando para todos nós o valor de se \\ncontrolar a energia, pois ele mesmo não sabe o \\nque ele é, ele mesmo não sabe como ser o que \\nele tem que ser, pois , para ele ser o que ele tem",
      "position": 58985,
      "chapter": 2,
      "page": 55,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.62245762711864,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 59.0,
        "avg_word_length": 4.758474576271187,
        "unique_word_ratio": 0.5677966101694916,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.13135593220338984,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "pois",
          "todos",
          "quântico",
          "evoluir",
          "matemática",
          "planeta",
          "terra",
          "mais",
          "fazer",
          "assim",
          "eles",
          "harmonia",
          "forma",
          "interpretar",
          "mesma",
          "como",
          "começou",
          "mostrar",
          "mesmo"
        ],
        "entities": [
          [
            "Joseph \\nClim",
            "PERSON"
          ],
          [
            "após muitos esforços",
            "PERSON"
          ],
          [
            "muito gasto de \\n",
            "PERSON"
          ],
          [
            "próprio excesso",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "amor",
            "GPE"
          ],
          [
            "humana",
            "ORG"
          ],
          [
            "para não",
            "PERSON"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "Terra",
            "PERSON"
          ]
        ],
        "readability_score": 69.07245762711864,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 134,
        "lexical_diversity": 0.5677966101694916
      },
      "preservation_score": 2.1671167735629094e-05
    },
    {
      "id": 1,
      "text": "que ser, todos no mundo tem que estar na \\nmesma frequência que Quântico, pois só assim \\nele circulará livremente.  \\nQuântico, sem saber o que fazer após tantos caos \\ngerado, começou a implementar a ideia de \\nliberdade, fazendo os pró prios humanos a \\nenxergarem que as suas regras foram mal \\ninterpretadas, assim Quântico começou a \\nimplementar regras contra as regras, fazendo os \\nhumanos captarem a energia de uma necessidade \\ncontra as regras, para se oporem de uma forma \\nàs vezes agressiva, porém necessária, \\nproporcional a própria evolução do próprio caos, \\nfazendo o humano enxergar e interpretar o \\npróprio erro em sua forma de viver, fazendo com \\nque alguns humanos que viveram uma vida um \\npouco mais turbulenta tivessem acesso a energia \\ndo Quânt ico de uma forma interpretativa perante \\no seu próprio viver, fazendo com que algumas \\npessoas com uma maior facilidade em ter acesso \\na energia do Quântico interpretassem um viver \\nproporcional ao seu próprio caos e a sua própria \\nfilosofia de vida.  \\nTemos Leon ardo da Vinci, Darwin, Newton, \\nNikolas Tesla, Einstein e muitos outros, não  \\nmencionarei um por um, se quiser se aprofundar \\nsobre a parte teórica da vida de Quântico, leia o \\nmeu livro O caos do passado sendo vivido no \\nfuturo . Fiz a minha propaganda, agora vamos \\ncontinuar com o Quântico, afinal ele é o super -",
      "position": 60489,
      "chapter": 2,
      "page": 56,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 36.46891891891892,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.5,
        "avg_word_length": 4.896396396396397,
        "unique_word_ratio": 0.6216216216216216,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.11261261261261261,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântico",
          "fazendo",
          "caos",
          "regras",
          "próprio",
          "humanos",
          "energia",
          "forma",
          "viver",
          "vida",
          "assim",
          "começou",
          "implementar",
          "contra",
          "proporcional",
          "própria",
          "acesso",
          "todos",
          "mundo",
          "mesma"
        ],
        "entities": [
          [
            "estar",
            "PRODUCT"
          ],
          [
            "suas regras",
            "PERSON"
          ],
          [
            "Quântico",
            "ORG"
          ],
          [
            "humanos captarem",
            "GPE"
          ],
          [
            "para se oporem de uma forma",
            "PERSON"
          ],
          [
            "humano enxergar e interpretar",
            "ORG"
          ],
          [
            "sua forma de viver",
            "PERSON"
          ],
          [
            "pouco mais",
            "PERSON"
          ],
          [
            "Quânt ico de uma forma interpretativa",
            "ORG"
          ],
          [
            "Quântico",
            "ORG"
          ]
        ],
        "readability_score": 70.78108108108108,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 138,
        "lexical_diversity": 0.6216216216216216
      },
      "preservation_score": 1.8175818100850208e-05
    },
    {
      "id": 1,
      "text": "herói desse livro, temos que exaltar o nosso \\nsenhor preconceito Quântico.  \\n Após algumas abordagens, Quântico via o \\nhumano se destruindo, entre eles mesmos, \\nporém Quântico pensava: olha o universo, temos \\ntantas estrelas brilhantes, temos tantas coisas \\nlindas e olha o tamanho do universo, veja como \\nele vive também, quem sou eu para falar dos \\nhumanos, no meu universo, na minha casa, eu \\ncomecei a me movimentar, gerei energia e forças , \\napós isso, eu nunca mais  tive um vazio, nunca \\nmais tive a ausência, nunca mais deixei de ser \\nalgo, pois até no universo o caos reina sobre tudo \\ne todos. Vejam o universo se expandindo, gera \\ncaos, explosões quânticas, buraco Negro, caos, \\nexplosões, expansão, adaptação, buraco negr o \\npara conter o excesso de energia, quasar, pois o \\npróprio buraco negro não consegue conter a \\nenergia ali concentrada, aumentando o próprio \\nuniverso para conseguir se adaptar ao próprio \\nuniverso. Quem sou eu para falar dos humanos, \\nse o próprio local de on de eu vim viver  em caos, \\naceitei o meu viver, aceitei o viver dos humanos, \\nirei me meter quando for necessário, no mais, eles \\nse adaptam sozinhos, irei implementar ideias \\nboas, ideias revolucionárias para eles enxergarem \\nque o meu mundo é tão caótico quanto  o deles, \\nvai que eles conseguem compreender o seu \\npróprio caos, conseguindo interpretar o meu caos \\ntambém.",
      "position": 61944,
      "chapter": 2,
      "page": 57,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.5,
      "complexity_metrics": {
        "word_count": 223,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.75,
        "avg_word_length": 5.0,
        "unique_word_ratio": 0.6278026905829597,
        "avg_paragraph_length": 223.0,
        "punctuation_density": 0.19282511210762332,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "universo",
          "caos",
          "próprio",
          "eles",
          "mais",
          "temos",
          "quântico",
          "humanos",
          "energia",
          "nunca",
          "buraco",
          "viver",
          "após",
          "olha",
          "tantas",
          "também",
          "quem",
          "falar",
          "tive",
          "pois"
        ],
        "entities": [
          [
            "herói desse livro",
            "ORG"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "humano se destruindo",
            "PERSON"
          ],
          [
            "eles mesmos",
            "PERSON"
          ],
          [
            "quem sou eu",
            "ORG"
          ],
          [
            "eu \\ncomecei",
            "PERSON"
          ],
          [
            "eu nunca mais",
            "PERSON"
          ],
          [
            "ausência",
            "GPE"
          ]
        ],
        "readability_score": 70.625,
        "semantic_density": 0,
        "word_count": 223,
        "unique_words": 140,
        "lexical_diversity": 0.6278026905829597
      },
      "preservation_score": 3.0060006859098423e-05
    },
    {
      "id": 1,
      "text": "Capítulo 15 foda -se \\nApós o Quântico direcionar o avanço tecnológico, \\nse repetiu o que já tinha acontecido, assim  como \\no Cesar destruiu boa parte d os humanos, o Hitler \\ntambém; assim como a peste negra destruiu boa \\nparte da população após o Cesar, após o Hitler \\nvieram várias pestes também.  \\nQuântico não estava entendendo e se perguntou:  \\n O que aconteceu dessa vez?  \\nOs humanos erraram novamente devido a sua \\nprópria evolução, não aprenderam nada com a \\nsua própria existência. Quântico parou, olhou e \\npercebeu que a culpa não era dele, a culpa era \\ndos próprios humanos que não conseguiam \\ncontrolar seus instintos básicos, assim como ele \\ntem a sua função de cicl os de fazer o bem, não \\nimporta a quem, os humanos também são assim, \\npois durante todos esses anos, durante toda a sua \\nexistência, quais foram as formas de interpretar o \\npróprio viver? Foi através da sua própria ganância \\nde ser mais, ter mais do que o outro  da própria \\nespécie, fazendo, assim, o seu caos e a sua \\nadaptação perante o seu próprio caos, Quântico, \\npor sua vez, olhou para tudo e para todos com \\num pensamento longe após ver as bombas \\natômicas explodirem, estava desanimado, um \\npouco triste e falou: quer saber, irei aproveitar a \\nminha vida, irei viver com os humanos sem regras,",
      "position": 63432,
      "chapter": 15,
      "page": 58,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 37.412328767123284,
      "complexity_metrics": {
        "word_count": 219,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 43.8,
        "avg_word_length": 4.707762557077626,
        "unique_word_ratio": 0.634703196347032,
        "avg_paragraph_length": 219.0,
        "punctuation_density": 0.1461187214611872,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "humanos",
          "após",
          "quântico",
          "própria",
          "como",
          "também",
          "cesar",
          "destruiu",
          "parte",
          "hitler",
          "estava",
          "existência",
          "olhou",
          "culpa",
          "durante",
          "todos",
          "próprio",
          "viver",
          "mais"
        ],
        "entities": [
          [
            "15",
            "CARDINAL"
          ],
          [
            "Após o Quântico direcionar",
            "ORG"
          ],
          [
            "já tinha acontecido",
            "PERSON"
          ],
          [
            "Cesar",
            "ORG"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "Cesar",
            "ORG"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "dessa vez",
            "PERSON"
          ],
          [
            "própria evolução",
            "PERSON"
          ]
        ],
        "readability_score": 76.68767123287671,
        "semantic_density": 0,
        "word_count": 219,
        "unique_words": 139,
        "lexical_diversity": 0.634703196347032
      },
      "preservation_score": 2.1478320859227506e-05
    },
    {
      "id": 1,
      "text": "me divertir, fazer aquilo que me der na telha, irei \\nviver para aprender a graça de um viver.  \\nQuântico, mais uma vez, resolveu viver entre os \\nhumanos após quase 200 mil anos, pois  ele estava \\ncom a mente dele mais aberta, não deve ser tão \\nmais difícil de viver agora do que antes, mostrarei \\npara os humanos a facilidade de um viver feliz . \\nQuântico estava determinado a ser feliz fazendo o \\nseu melhor, mostrando confiança, caráter, \\ndigni dade, amor, respeito e, acima de tudo, ser \\ndigno.  \\nMas como viverei o sentimento do humano?  \\nComo posso mostrar aos humanos como serem \\nseres humanos?  \\nQuântico, com a sua sabedoria, enxergou que, em \\nsua própria vida, ele teve que viver para \\naprender, assim Quântico pensou em nascer, \\nviver e morrer igual a um humano, qual a forma \\nhumana que eu tenho que ser para ser o exemplo \\nque eu quero ser?  \\nQuântico pa rou para analisar tudo que viveu e \\npensou: tudo que eu fiz gerou preconceito, \\nguerras, atritos, julgamentos, menosprezo, quais \\nforam as pessoas mais afetadas?  \\nViverei de forma que todos entendam que o seu \\nviver é igual ao meu, pois somos frutos de uma \\nnece ssidade básica de viver em harmonia com o",
      "position": 64831,
      "chapter": 2,
      "page": 59,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.00972906403941,
      "complexity_metrics": {
        "word_count": 203,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 25.375,
        "avg_word_length": 4.615763546798029,
        "unique_word_ratio": 0.6502463054187192,
        "avg_paragraph_length": 203.0,
        "punctuation_density": 0.1724137931034483,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "quântico",
          "mais",
          "humanos",
          "tudo",
          "como",
          "aprender",
          "pois",
          "estava",
          "feliz",
          "viverei",
          "humano",
          "pensou",
          "igual",
          "forma",
          "divertir",
          "fazer",
          "aquilo",
          "telha",
          "irei"
        ],
        "entities": [
          [
            "200",
            "CARDINAL"
          ],
          [
            "dele mais aberta",
            "PERSON"
          ],
          [
            "tão \\nmais difícil de viver",
            "PRODUCT"
          ],
          [
            "dade",
            "GPE"
          ],
          [
            "amor",
            "GPE"
          ],
          [
            "acima de tudo",
            "PERSON"
          ],
          [
            "mostrar aos humanos",
            "PERSON"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "eu quero ser",
            "PERSON"
          ],
          [
            "Quântico pa rou",
            "PERSON"
          ]
        ],
        "readability_score": 85.9277709359606,
        "semantic_density": 0,
        "word_count": 203,
        "unique_words": 132,
        "lexical_diversity": 0.6502463054187192
      },
      "preservation_score": 2.1936332190681292e-05
    },
    {
      "id": 1,
      "text": "planeta Terra e, automaticamente, com o \\nuniverso, se nós não conseguimos enxergar que \\ntodos nós somos o que temos que ser, como \\npodemos ser o que devemos ser se não sabemos \\nser? Nascerei em uma mulher negra junto a  um \\npai branco, serei  uma mulher negra em um meio \\nsocial em que eu posso poder crescer como \\npessoa e evoluir o meu próprio aprendizado com \\nos erros humanos.  \\nNascerei com caraterísticas  vinda no nosso DNA \\neuropeu junto a um DNA Negro, assim viverei em \\num país onde tenham várias pessoas de diferentes \\nlocais do mundo, onde as pessoas vivem com \\nvariedades religiosa, estrutural, familiar, sexo, \\natritos, beleza, natureza, calor humano e muita s \\noutras coisas que o humano foi adquirindo no \\ndecorrer da sua existência, nascerei no Brasil ou \\nMéxico?  \\nEle ficou nessa dúvida, pois um é semelhante ao \\noutro culturalmente, entretanto o México é no \\nhemisfério norte, e o hemisfério norte já tem \\nmuita facil idade em um viver melhor que o \\nhemisfério sul; no hemisfério norte é mais fácil \\nter algo, pois até para se comercializar entre eles \\né mais acessível devido a distância, a evolução \\nnos países no entorno do México facilita a \\npossibilidade de existir comércio , lá a língua que \\neles falam os ajuda a evoluir mais fácil, pois \\noutros países falam o espanhol mais do que falam \\na língua portuguesa, nascerei no Brasil, pois lá a",
      "position": 66119,
      "chapter": 3,
      "page": 60,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 38.425,
      "complexity_metrics": {
        "word_count": 232,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 58.0,
        "avg_word_length": 4.75,
        "unique_word_ratio": 0.6293103448275862,
        "avg_paragraph_length": 232.0,
        "punctuation_density": 0.1206896551724138,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nascerei",
          "pois",
          "hemisfério",
          "mais",
          "méxico",
          "norte",
          "falam",
          "como",
          "mulher",
          "negra",
          "junto",
          "evoluir",
          "onde",
          "pessoas",
          "humano",
          "muita",
          "brasil",
          "fácil",
          "eles",
          "países"
        ],
        "entities": [
          [
            "nós não conseguimos enxergar que",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "que devemos",
            "PERSON"
          ],
          [
            "se não sabemos",
            "PERSON"
          ],
          [
            "que eu posso",
            "PERSON"
          ],
          [
            "Negro",
            "ORG"
          ],
          [
            "calor humano e muita",
            "ORG"
          ],
          [
            "outras coisas",
            "PERSON"
          ],
          [
            "humano foi",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ]
        ],
        "readability_score": 69.575,
        "semantic_density": 0,
        "word_count": 232,
        "unique_words": 146,
        "lexical_diversity": 0.6293103448275862
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "galera está longe do restante dos outros países, \\neles tiveram que se adaptar entre eles mes mos, \\nfazendo ter mais plantio, mais gado e mais \\nvariedades de pessoas do que no México e a \\nlíngua portuguesa faz eu me expressar melhor \\ncom o meu sentimento, devido a quantidade de \\npalavras proporcionais ao que eu quero expressar, \\nrelativo ao que eu estou vivendo; os outros países \\nnão conseguem se expressar com mais variedades \\nde palavras, os tornando pessoas mais \\ndirecionadas e mais secas, devido a não conseguir \\nse expressarem melhor.",
      "position": 67602,
      "chapter": 3,
      "page": 61,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.49325842696629,
      "complexity_metrics": {
        "word_count": 89,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 89.0,
        "avg_word_length": 4.977528089887641,
        "unique_word_ratio": 0.6741573033707865,
        "avg_paragraph_length": 89.0,
        "punctuation_density": 0.10112359550561797,
        "line_break_count": 11,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "expressar",
          "outros",
          "países",
          "eles",
          "variedades",
          "pessoas",
          "melhor",
          "devido",
          "palavras",
          "galera",
          "está",
          "longe",
          "restante",
          "tiveram",
          "adaptar",
          "entre",
          "fazendo",
          "plantio",
          "gado"
        ],
        "entities": [
          [
            "mes mos",
            "PERSON"
          ],
          [
            "México",
            "GPE"
          ],
          [
            "faz eu",
            "PERSON"
          ],
          [
            "que eu quero",
            "PERSON"
          ],
          [
            "eu estou vivendo",
            "PERSON"
          ],
          [
            "outros países",
            "ORG"
          ],
          [
            "secas",
            "GPE"
          ],
          [
            "se expressarem melhor",
            "PERSON"
          ]
        ],
        "readability_score": 54.00674157303371,
        "semantic_density": 0,
        "word_count": 89,
        "unique_words": 60,
        "lexical_diversity": 0.6741573033707865
      },
      "preservation_score": 2.3864800954697224e-06
    },
    {
      "id": 1,
      "text": "Capítulo 16 uma nova vida  \\nO nosso herói veio ao nosso mundo na década de  \\n80, logo após um regime militar e na maior \\nascensão tecnológica no mundo todo, o Quântico \\ndeixou o seu nome para trás e virou Quântica!  \\nA Quântica nasceu uma menina com o cabelo \\ncrespo e enrolado tipo black , olhos azuis e a cor \\nda pele dela era uma negra reluzente, parecia um \\nanjo.  \\nAssim que ela nasceu, sua mãe a pegou nos \\nbraços, olhou para ela e falou: você será a energia \\nque moverá a minha vida para algo maior do que \\neu possa imaginar.  \\nSeu pai já era um cara “menos amoroso”, não era \\nmuito de falar sobre  os seus sentimentos, mas, \\nquando a pegou nos braços, o olhar dele dizia \\ntudo que a mãe dela precisava, pois, ali, ela via \\namor verdadeiro, um amor que ele deixou bem \\nclaro em seu olhar, só abandonaria a Quântica \\natravés da morte.  \\nQuântica, ao ser pega no colo, se sentiu segura, \\nse sentiu amada, sentiu o aconchego ( Ato ou \\nefeito de aconchegar. Acolhimento, amparo físico \\njunto a alguém ou algo; abraço. Aconchego é a \\nmelhor forma de expressar o sentimento de amar \\nao tocar quem você realmente ama. ) e, a partir  \\ndesse momento, sentiu uma energia de proteção \\ndiante de um viver, nada nem ninguém",
      "position": 68285,
      "chapter": 16,
      "page": 62,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 31.173648648648648,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.75,
        "avg_word_length": 4.328828828828829,
        "unique_word_ratio": 0.7027027027027027,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.14414414414414414,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "sentiu",
          "vida",
          "nosso",
          "mundo",
          "maior",
          "deixou",
          "nasceu",
          "dela",
          "pegou",
          "braços",
          "você",
          "energia",
          "algo",
          "olhar",
          "amor",
          "aconchego",
          "capítulo",
          "nova",
          "herói"
        ],
        "entities": [
          [
            "16",
            "CARDINAL"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "herói veio",
            "PERSON"
          ],
          [
            "virou Quântica",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "ela nasceu",
            "PERSON"
          ],
          [
            "sua",
            "ORG"
          ],
          [
            "braços",
            "GPE"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "para ela",
            "PERSON"
          ]
        ],
        "readability_score": 84.82635135135135,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 156,
        "lexical_diversity": 0.7027027027027027
      },
      "preservation_score": 2.343089548279364e-05
    },
    {
      "id": 1,
      "text": "conseguiria tirar aquele sentimento que ali foi \\nproduzido, a conexão entre ela e sua mãe, após \\nser amamentada, ficou ainda maior, pois parecia \\nque a energia da Quântica jun to a sua mãe era \\numa única coisa, em total harmonia, uma \\nprofundidade em se sentir em paz e em \\nsegurança que nada e ninguém conseguiria \\ndesfazer e, naquele mesmo momento, percebeu \\na fragilidade de se ter uma vida dependendo de \\noutro humano.  \\nQuântica nasceu  em uma família em um bairro \\nque continha muitas crianças, os pais tinham \\nmuitos amigos, “tudo em sua volta tinha o lado \\nruim com coisas boas e o lado bom com coisas \\nruins”. Nos primeiros dias em sua nova jornada, \\nQuântica aprendeu o valor de ser amada por  uma \\nmãe e um pai, aprendeu o valor de se sentir \\nsegura sem depender só de si mesma. Quando a \\nQuântica era Quântico e viveu em meio aos \\n“humanos”, não se tinha noção do que era sentir \\no sentimento, só se tinha razão de se fazer o \\n“certo”  sem ter prazer devido ao mesmo \\nentender que era o melhor a ser feito perante a \\nsituação a qual se estava vivendo, pois a conexão \\ndo Quântico com o planeta Terra era sentida e, só \\ndepois de alguns anos, ele vivendo entre os \\nhumanos, que ele esqueceu de sentir a conexão \\nque e le tinha com o planeta Terra.  \\nQuântica e seus pais saíram da maternidade em \\ndireção a sua casa. Ao chegar em sua nova casa,",
      "position": 69618,
      "chapter": 3,
      "page": 63,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.374493927125506,
      "complexity_metrics": {
        "word_count": 247,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.166666666666664,
        "avg_word_length": 4.352226720647773,
        "unique_word_ratio": 0.562753036437247,
        "avg_paragraph_length": 247.0,
        "punctuation_density": 0.09716599190283401,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "sentir",
          "tinha",
          "conexão",
          "conseguiria",
          "sentimento",
          "entre",
          "pois",
          "mesmo",
          "pais",
          "lado",
          "coisas",
          "nova",
          "aprendeu",
          "valor",
          "quântico",
          "humanos",
          "vivendo",
          "planeta",
          "terra"
        ],
        "entities": [
          [
            "ela e sua mãe",
            "PERSON"
          ],
          [
            "após \\nser amamentada",
            "PERSON"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "valor de ser amada",
            "ORG"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "só de si",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ]
        ],
        "readability_score": 78.11099865047234,
        "semantic_density": 0,
        "word_count": 247,
        "unique_words": 139,
        "lexical_diversity": 0.562753036437247
      },
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "id": 1,
      "text": "Quântica se sentiu acolhida e segura naquele \\nespaço em que ela ia viver uma parte da sua vida, \\npois, naquela casa, os seus pais deco raram tudo \\ncom muito esforço, dedicação, carinho, amor, \\nsentimento e com tudo que um lar poderia \\noferecer para fazê -la se sentir segura, a energia \\nde sua casa era algo que ela não sabia explicar, \\nela simplesmente sentia que poderia ter \\nliberdade ali naquel a casa.  \\nQuântica chorava quando defecava, Quântica \\nchorava ao necessitar de alimento, Quântica \\nchorava quando tinha dor, Quântica se \\ncomunicava através do choro para os pais \\nsaberem o que ela necessitava e, por muitas \\nvezes, os seus pais sendo inexperiente s em cuidar \\nde um filho mais a dificuldade em ter comida, \\nmanter a casa, pagar as contas, por muitas vezes \\nnão tinham o que era “necessário” para se ter \\numa vida “melhor”. Entretanto, Quântica, sendo \\numa bebê só sentia o sentimento da vida, não \\nentendia na da da vida, só conseguia sobreviver \\ndevido aos pais dela cuidarem dela, e ela, por sua \\nvez, foi crescendo dentro desse lar, com muita \\ndificuldade em um viver e muito amor para se \\nviver.  \\nO quarto de Quântica era como de qualquer \\nmenina em que os seus pais p odem decorar, de \\nacordo com uma menina cuidada com todo amor \\ne carinho.",
      "position": 71089,
      "chapter": 3,
      "page": 64,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 37.30642201834863,
      "complexity_metrics": {
        "word_count": 218,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 54.5,
        "avg_word_length": 4.660550458715596,
        "unique_word_ratio": 0.5963302752293578,
        "avg_paragraph_length": 218.0,
        "punctuation_density": 0.13761467889908258,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "pais",
          "vida",
          "casa",
          "viver",
          "seus",
          "amor",
          "chorava",
          "segura",
          "tudo",
          "muito",
          "carinho",
          "sentimento",
          "poderia",
          "sentia",
          "quando",
          "muitas",
          "vezes",
          "sendo",
          "dificuldade"
        ],
        "entities": [
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "naquela casa",
            "PERSON"
          ],
          [
            "seus pais deco raram tudo \\n",
            "ORG"
          ],
          [
            "muito esforço",
            "PERSON"
          ],
          [
            "para fazê -la se",
            "PERSON"
          ],
          [
            "ela não sabia explicar",
            "PERSON"
          ],
          [
            "ela simplesmente sentia",
            "PERSON"
          ],
          [
            "ali naquel",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "chorava quando defecava",
            "PERSON"
          ]
        ],
        "readability_score": 71.35183486238532,
        "semantic_density": 0,
        "word_count": 218,
        "unique_words": 130,
        "lexical_diversity": 0.5963302752293578
      },
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "id": 1,
      "text": "A cortina de seu quarto era rosa intangível com \\numa cortina branca atrás para impedir o excesso \\nde sol, havia  um berço branco com lençóis rosa e \\nedredom lilás com imagens dos ursinhos  \\ncarinhosos. Acima do seu berço, tinha um \\ncarrossel de pôneis coloridos, e as suas roupas, na \\nmaioria das vezes, eram vestidos estilo as das \\nprincesas da Disney, com um pequeno laço, presa \\na uma rosa no arco para prender os seus cabelos.",
      "position": 72469,
      "chapter": 3,
      "page": 65,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.134,
      "complexity_metrics": {
        "word_count": 75,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 37.5,
        "avg_word_length": 4.613333333333333,
        "unique_word_ratio": 0.7866666666666666,
        "avg_paragraph_length": 75.0,
        "punctuation_density": 0.12,
        "line_break_count": 8,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "rosa",
          "cortina",
          "berço",
          "quarto",
          "intangível",
          "branca",
          "atrás",
          "impedir",
          "excesso",
          "havia",
          "branco",
          "lençóis",
          "edredom",
          "lilás",
          "imagens",
          "ursinhos",
          "carinhosos",
          "acima",
          "tinha",
          "carrossel"
        ],
        "entities": [
          [
            "excesso \\nde sol",
            "PERSON"
          ],
          [
            "berço branco",
            "ORG"
          ],
          [
            "Acima",
            "PERSON"
          ],
          [
            "suas roupas",
            "PERSON"
          ],
          [
            "da Disney",
            "PERSON"
          ],
          [
            "pequeno laço",
            "PERSON"
          ],
          [
            "arco",
            "ORG"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "seus cabelos",
            "ORG"
          ]
        ],
        "readability_score": 79.866,
        "semantic_density": 0,
        "word_count": 75,
        "unique_words": 59,
        "lexical_diversity": 0.7866666666666666
      },
      "preservation_score": 1.7356218876143437e-06
    },
    {
      "id": 1,
      "text": "Capítulo 17 aprend endo  \\nAos 6 meses de idade, a Quântica estava \\ncomeçando a ficar em pé, dando pequenos \\npassos e aprendendo a distinguir palavras e sons \\ndiferentes, dando importância para os tons das \\npalavras que seu pai e sua mãe proferiam \\nenquanto davam esporros, ficando m ais fácil \\nsentir o sentimento do seu pai e de sua mãe \\nperante o seu próprio erro, cada vez que ela \\npegava algo que não era para pegar, sua mãe e \\nseu pai brigavam com ela e, assim, começava a \\naprender o que é erro e acerto, ganhar e perder.  \\n Cada vez que nó s, humanos, temos dificuldades \\nem ter algo, nós aprendemos a lutar de acordo \\ncom o nosso querer aquele aprendizado, fazendo \\npercebermos a importância de termos uma \\nestrutura familiar e um meio de viver necessário \\npara se ter um viver melhor em uma vida, \\npodendo ser qualquer pessoa que possa \\ndirecionar as suas ações futuras para melhores \\nações em um viver melhor posteriormente.  \\nEm seu primeiro aniversário, Quântica estava \\numa menina linda, com um sorriso para todos \\naqueles com quem ela se sentia à vontade, \\nsimpática, amorosa e muito agitada, pois naquela \\népoca ela já estava caminhando há 3 meses, \\nsendo fácil e hábil em se movimentar entre as \\npernas das pessoas, pegar as coisas em cima da \\nmesa. Ela era uma menina com muita saúde e",
      "position": 73044,
      "chapter": 17,
      "page": 66,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.37973568281939,
      "complexity_metrics": {
        "word_count": 227,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 56.75,
        "avg_word_length": 4.599118942731278,
        "unique_word_ratio": 0.6519823788546255,
        "avg_paragraph_length": 227.0,
        "punctuation_density": 0.10572687224669604,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estava",
          "viver",
          "meses",
          "quântica",
          "dando",
          "palavras",
          "importância",
          "fácil",
          "erro",
          "cada",
          "algo",
          "pegar",
          "melhor",
          "ações",
          "menina",
          "capítulo",
          "aprend",
          "endo",
          "idade",
          "começando"
        ],
        "entities": [
          [
            "17",
            "CARDINAL"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "tons das \\npalavras",
            "PERSON"
          ],
          [
            "ais fácil \\n",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "cada vez",
            "ORG"
          ],
          [
            "ela \\npegava algo que",
            "PERSON"
          ],
          [
            "sua mãe",
            "ORG"
          ],
          [
            "Cada vez",
            "PERSON"
          ]
        ],
        "readability_score": 70.24526431718061,
        "semantic_density": 0,
        "word_count": 227,
        "unique_words": 148,
        "lexical_diversity": 0.6519823788546255
      },
      "preservation_score": 1.6199137617733874e-05
    },
    {
      "id": 1,
      "text": "muito amor em seu entorno e, em seu aniversário \\nde um ano, não poderia ser diferente, toda a sua \\nfamília ajudou a fazer um aniversário com a \\ntemática da Peppa Pig , pois quando ela se \\nsentava em frente à televisão e passava essa \\nanimação, ela se concentrava e não atrapalhava o \\npai a cu idar dela, pois a mãe trabalhava como \\nvendedora em uma grande empresa, o pai \\ntrabalhava home office em uma empresa de web \\ndesigner pequena, não muito reconhecida e \\npouco remunerada, a mãe era o pilar da família \\nno quesito monetário, fazendo assim o pai e a  \\nmãe da Quântica chegarem a um acordo sobre a \\nevolução profissional da família, ficaria a cargo da \\nmãe de Quântica, pois a chance de ela ter uma \\ncondição financeira maior para a família era mais \\nacessível.  \\nNesse aniversário de um ano de Quântica, ela \\nbrinc ava com outras crianças de correr, pegar \\nchinelos dos pais, pula -pula, salgadinhos, \\nrefrigerantes e todos os tipos de pessoas que se \\npossa pensar, de estilo de vida diferentes \\nestavam presentes: o tio da Quântica namorava \\num outro homem, esse tio da Quânti ca era o \\npadrinho dela, pois o pai de Quântica e o tio são \\namigos desde que o pai nasceu, pois o seu tio era \\nmais velho que o seu pai, ele era uma pessoa \\nsorridente demais, vivia animando a todos em sua \\nvolta com suas histórias engraçadas de quando \\nera um adolescente, ele sempre falava que o",
      "position": 74462,
      "chapter": 3,
      "page": 67,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.510931174089066,
      "complexity_metrics": {
        "word_count": 247,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 123.5,
        "avg_word_length": 4.469635627530365,
        "unique_word_ratio": 0.5668016194331984,
        "avg_paragraph_length": 247.0,
        "punctuation_density": 0.10526315789473684,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "quântica",
          "família",
          "aniversário",
          "muito",
          "quando",
          "dela",
          "trabalhava",
          "empresa",
          "mais",
          "pula",
          "todos",
          "amor",
          "entorno",
          "poderia",
          "diferente",
          "toda",
          "ajudou",
          "fazer",
          "temática"
        ],
        "entities": [
          [
            "muito amor",
            "PERSON"
          ],
          [
            "quando ela se \\nsentava",
            "PERSON"
          ],
          [
            "televisão e passava",
            "PERSON"
          ],
          [
            "essa \\nanimação",
            "ORG"
          ],
          [
            "ela se concentrava e não atrapalhava",
            "PERSON"
          ],
          [
            "não muito reconhecida e \\npouco remunerada",
            "PERSON"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "financeira maior",
            "PERSON"
          ],
          [
            "tipos de pessoas",
            "ORG"
          ]
        ],
        "readability_score": 36.90910931174089,
        "semantic_density": 0,
        "word_count": 247,
        "unique_words": 140,
        "lexical_diversity": 0.5668016194331984
      },
      "preservation_score": 1.8874888027805986e-05
    },
    {
      "id": 1,
      "text": "amor não é sobre um homem, mulher, gay, \\nlésbica, travesti,  falava que o amor é para ser \\nvivido e sentido, se você não sente isso, é sinal de \\nque você não confia na pessoa que você quer \\nviver a sua vida toda, pois, quan do ele era mais \\nnovo, tentou ficar com uma menina, ambos eram \\nnovos, e ele vivia sendo excluído da roda de \\namigos, pois todos julgavam o seu \\ncomportamento mais aflorado, que parecia um \\npadrão para o lado feminino de um \\ncomportamento humano, quase todos os amigos \\n“meninos” não tinham coragem de andar ao lado \\ndele, e o pai da Quântica sempre o olhou como \\numa pessoa forte e de personalidade. Quando \\ncomeçou a namorar essa menina, o tio de \\nQuântica não conseguia se sentir à vontade e, \\npor, mas que tivesse admiraç ão, ele não \\nconseguia se sentir “confortável' ao lado dela, \\npois não sentia os desejos carnais, ele sentia \\nadmiração, empatia, confiança, amizade, tudo \\nque um ser humano precisa para ser feliz em um \\nrelacionamento adolescente, pois as brincadeiras, \\nas conv ersas, o gosto eram muito semelhantes \\naos da menina. Após o término do namoro com \\nessa menina, após ambos conversarem e \\nchegarem a um entendimento de que a amizade \\nseria o melhor para ambos, ele assumiu gostar de \\nhomens, já que ele conheceu o marido dele n o \\ntrabalho dele enquanto ainda estava namorando. \\nQuando ele conheceu o marido dele em uma \\nempresa de menor aprendiz, o tempo parou, o",
      "position": 75959,
      "chapter": 3,
      "page": 68,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.38414634146341,
      "complexity_metrics": {
        "word_count": 246,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 61.5,
        "avg_word_length": 4.6138211382113825,
        "unique_word_ratio": 0.6097560975609756,
        "avg_paragraph_length": 246.0,
        "punctuation_density": 0.15040650406504066,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "menina",
          "dele",
          "você",
          "ambos",
          "lado",
          "amor",
          "pessoa",
          "mais",
          "eram",
          "amigos",
          "todos",
          "comportamento",
          "humano",
          "quântica",
          "quando",
          "essa",
          "conseguia",
          "sentir",
          "sentia"
        ],
        "entities": [
          [
            "amor não",
            "ORG"
          ],
          [
            "para ser \\nvivido",
            "PERSON"
          ],
          [
            "você não sente",
            "ORG"
          ],
          [
            "quan",
            "GPE"
          ],
          [
            "novo",
            "GPE"
          ],
          [
            "novos",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "lado feminino",
            "PERSON"
          ],
          [
            "lado \\ndele",
            "PERSON"
          ]
        ],
        "readability_score": 67.8658536585366,
        "semantic_density": 0,
        "word_count": 246,
        "unique_words": 150,
        "lexical_diversity": 0.6097560975609756
      },
      "preservation_score": 2.965020724674504e-05
    },
    {
      "id": 1,
      "text": "olhar dele era de encanto, cada sorriso, cada \\nexpressão que ele olhava daquele homem o fazia \\npensar a quão bela  é a paixão , ele se sentiu \\natraído por aquele humano no momento em que \\nele olhou em seus olhos e notou a conexão da \\ntroca de olhar, nesse momento, o destino nos \\nmostra coisas que se não percebermos, seguimos \\numa estrada totalmente diferente na vida.  \\nO tio  e o namorad o, fizeram a decoração da festa \\ne pagaram tudo que usaram na decoração, tudo \\nficou lindo, pois o seu tio gostava da cor rosa, \\ngostava de deixar tudo bem decorado e alinhado, \\npois ele é uma pessoa muito organizada e limpa, \\ntudo de seu tio tem um motivo para  estar em \\ndeterminado lugar, tudo que o seu tio faz tem um \\npropósito de fazer um melhor para um contexto.  \\nOs avós de Quântica por parte de sua mãe eram \\nnegros e amavam escola de samba; todos os \\ndomingos, eles iam para a quadra da Império \\nSerrano comer uma feijoada, beber uma cerveja, \\nfumar um baseado, ver os amigos, sambar e viver \\nas lembranças que trouxeram muitas felicidades \\npara os seus avós, que se conheceram na própria \\nquadra da escola de samba. Na época, o Brasil \\nestava passando por um regime militar muito \\nintenso, todos no Rio de Janeiro tinham que \\nseguir uma conduta militar cheia de regras e \\nrestrições, ao mesmo tempo, negros começarem \\na ter mais voz na sociedade, os avós maternos de \\nQuântica eram pessoas de uma mente aberta a",
      "position": 77486,
      "chapter": 3,
      "page": 69,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.33754940711462,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 63.25,
        "avg_word_length": 4.458498023715415,
        "unique_word_ratio": 0.6284584980237155,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.11067193675889328,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "avós",
          "olhar",
          "cada",
          "momento",
          "seus",
          "decoração",
          "pois",
          "gostava",
          "muito",
          "quântica",
          "eram",
          "negros",
          "escola",
          "samba",
          "todos",
          "quadra",
          "militar",
          "dele",
          "encanto"
        ],
        "entities": [
          [
            "olhar dele era de encanto",
            "PERSON"
          ],
          [
            "cada sorriso",
            "ORG"
          ],
          [
            "cada",
            "GPE"
          ],
          [
            "expressão",
            "ORG"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "mostra coisas",
            "NORP"
          ],
          [
            "uma estrada",
            "ORG"
          ],
          [
            "gostava da cor rosa",
            "PERSON"
          ],
          [
            "gostava de deixar",
            "PERSON"
          ],
          [
            "organizada e limpa",
            "ORG"
          ]
        ],
        "readability_score": 67.03745059288538,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 159,
        "lexical_diversity": 0.6284584980237155
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "tudo e frequentavam o t erreiro de macumba que \\nos seus pais frequentavam, ali eles sentiam uma \\nenergia surreal que os alimentavam em aceitar \\num viver melhor, dentro de todo o caos que \\nestava acontecendo. Os avós maternos de \\nQuântica só tiveram a mãe de Quântica, pois, \\nquando sua mãe nasceu, sua avó teve \\ncomplicações e não pôde ter mais filhos.  \\nOs avós paternos eram europeus e vieram parar \\naqui no Brasil em forma de refúgio da guerra que \\nacontecia em seu país. Os avós paternos \\ncontinham muitos estereótipos preconceituosos \\nde um viv er europeu, porém eles tinham uma \\nmente aberta, eram céticos e, devido a tudo que \\nviveram na Europa: uma Europa cheia de \\nmanifestações pela liberdade, gerando guerras e \\nconflitos de interesses diferentes de um país para \\ncom outro, de um país ter mais, ser mais, querer \\nmais. Os avós paternos de Quântica, ao chegarem \\nao Brasil, não sabiam como viver, pois sofriam \\nmuitos preconceitos por serem brancos \\neuropeus, ricos... E os seus avós passavam fome e \\nnecessidade por não conseguirem falar a língua \\ndireito, não conseguiam se sustentar \\ncorretamente e, devido a sua aparência, eles não \\narrumavam trabalho, pois as pessoas que \\nnecessitavam de alguém para trabalhar como \\nfaxineira, pedreiro, lavador e qualquer trabalho, e \\nnão emprego, os julgavam devido a aparência \\nbran ca, olhos claros, cabelos loiros; para esse tipo",
      "position": 79016,
      "chapter": 3,
      "page": 70,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.18139880952381,
      "complexity_metrics": {
        "word_count": 224,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.333333333333336,
        "avg_word_length": 5.049107142857143,
        "unique_word_ratio": 0.6696428571428571,
        "avg_paragraph_length": 224.0,
        "punctuation_density": 0.15625,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "avós",
          "mais",
          "eles",
          "quântica",
          "pois",
          "paternos",
          "país",
          "devido",
          "tudo",
          "frequentavam",
          "seus",
          "viver",
          "eram",
          "europeus",
          "brasil",
          "muitos",
          "europa",
          "como",
          "aparência",
          "trabalho"
        ],
        "entities": [
          [
            "ali eles sentiam uma",
            "PERSON"
          ],
          [
            "dentro de todo o caos que \\nestava",
            "ORG"
          ],
          [
            "mãe de Quântica",
            "GPE"
          ],
          [
            "quando sua",
            "PERSON"
          ],
          [
            "mãe nasceu",
            "FAC"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "sofriam \\nmuitos preconceitos",
            "PERSON"
          ]
        ],
        "readability_score": 79.81860119047619,
        "semantic_density": 0,
        "word_count": 224,
        "unique_words": 150,
        "lexical_diversity": 0.6696428571428571
      },
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "id": 1,
      "text": "de trabalho a aparência deles era um  julgamento \\npor serem “muito” para o próprio trabalho.  \\nA festa de um ano de Quântica era uma total \\nharmonia, tudo e todos pareciam estar na mesma \\nfrequência, pois a luta em um viver das famílias \\nfoi tão grande que o fazer uma festa para \\nQuântica foi o marco de uma conquista para \\nambas as famílias, pois nenhum membro havia \\nconseguido  viver tão bem perante uma conquista \\nde viver em prol da família.  \\nApós esse aniversário de um ano, parecia que \\ntudo estava indo para um melhor caminho de \\nviver para todos, pois os avós estavam \\naposentados, os pais e o tio de Quântica estavam \\ntrabalhando e conseguindo viver bem dentro de \\num contexto, tudo para a Quântica ter um \\ncrescimento saudáv el e feliz.  \\nQuântica começou a ir para a creche, pois o seu \\npai começou a ir para o escritório trabalhar, na \\ncreche, a Quântica tinha muitos amiguinhos que \\nestavam aprendendo e evoluindo de forma \\ndiferente, Quântica não entendia essa diferença, \\nela era uma  criança curiosa e olhava para as \\ncrianças chorando, correndo, e ela ali, querendo \\nentender com quem brincar, perdida no seu \\npróprio pensamento sobre o que fazer. Corro? \\nChoro? Fico parada?  \\nQuântica com esse “caos” não sabia o que fazer e \\ncomeçou a se adap tar, falar mais, brincar com",
      "position": 80516,
      "chapter": 3,
      "page": 71,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.70254524886878,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.625,
        "avg_word_length": 4.701357466063349,
        "unique_word_ratio": 0.579185520361991,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.11312217194570136,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "viver",
          "pois",
          "tudo",
          "fazer",
          "estavam",
          "começou",
          "trabalho",
          "próprio",
          "festa",
          "todos",
          "famílias",
          "conquista",
          "esse",
          "creche",
          "brincar",
          "aparência",
          "deles",
          "julgamento",
          "serem"
        ],
        "entities": [
          [
            "serem “muito",
            "PERSON"
          ],
          [
            "para",
            "PERSON"
          ],
          [
            "pareciam estar",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "marco de uma conquista",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "tudo estava",
            "PERSON"
          ],
          [
            "de Quântica",
            "GPE"
          ],
          [
            "tudo para",
            "PERSON"
          ],
          [
            "Quântica",
            "FAC"
          ]
        ],
        "readability_score": 84.77709276018099,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 128,
        "lexical_diversity": 0.579185520361991
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "amigos que ela se sentia melhor, pedir e, quando \\npedia e não era atendida, chorava e, por muitas \\nvezes, ela não recebia, pois não era certo receber \\ntão fácil, ou mesmo não poderia ter por causa da \\nidade, ou por dinheiro e, quan do recebia as coisas \\natravés de chorar, ela entendia o valor do ganhar. \\nQuântica, por ser esperta, entendeu o valor de se \\ncomunicar para ter as coisas que ela precisava, \\npercebeu que, quando ela conversava, ela recebia \\nmais as vontades dela do que quando c horava, \\nassim começou a ter sagacidade ( qualidade ou \\nvirtude de sagaz; aptidão para compreender ou \\naprender por simples indícios. Agudeza de \\nespírito; argúcia, manha, malícia,  entender o \\nmomento a qual está vivendo e saber viver o \\nmelhor no mesmo momento.)  em conversar, \\nargumentar, perguntar, questionar, sentir, \\npriorizar, direcionar e gerar um caráter maior \\nperante a sua própria personalidade.",
      "position": 81926,
      "chapter": 3,
      "page": 72,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.00408163265306,
      "complexity_metrics": {
        "word_count": 147,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 36.75,
        "avg_word_length": 5.01360544217687,
        "unique_word_ratio": 0.7006802721088435,
        "avg_paragraph_length": 147.0,
        "punctuation_density": 0.2108843537414966,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "recebia",
          "melhor",
          "mesmo",
          "coisas",
          "valor",
          "momento",
          "amigos",
          "sentia",
          "pedir",
          "pedia",
          "atendida",
          "chorava",
          "muitas",
          "vezes",
          "pois",
          "certo",
          "receber",
          "fácil",
          "poderia"
        ],
        "entities": [
          [
            "ela se sentia melhor",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "ela não recebia",
            "PERSON"
          ],
          [
            "recebia",
            "GPE"
          ],
          [
            "ela entendia",
            "PERSON"
          ],
          [
            "coisas",
            "NORP"
          ],
          [
            "ela precisava",
            "PERSON"
          ],
          [
            "quando ela conversava",
            "PERSON"
          ],
          [
            "ela recebia \\nmais",
            "PERSON"
          ],
          [
            "que quando",
            "PERSON"
          ]
        ],
        "readability_score": 80.12091836734695,
        "semantic_density": 0,
        "word_count": 147,
        "unique_words": 103,
        "lexical_diversity": 0.7006802721088435
      },
      "preservation_score": 1.4318880572818336e-05
    },
    {
      "id": 1,
      "text": "Capítulo 1 8 início de um viver  \\nA partir dos seus 5, 6, 7 anos, Quântica já \\nentendia e sabia sobre algumas coisas que a \\ndeixavam feliz, algumas coisas que a deixavam \\ntriste, algumas comidas, algumas pessoas que ela \\nadmirava, sabia a diferença entre quem ela \\namava e quem ela não amava. Começou a \\nconstruir suas memórias construtivas ( se criam \\npela constância de s e fazer: memória repetitiva, \\nusar banheiro, tomar banho, escovar os dentes, \\ncomer, beber e etcétera. ), ter suas manias, seus \\ncostumes, sua rotina. Tudo em sua vida já estava \\nindo em uma direção de um caráter, pois a \\nQuântica teve uma família que sempre \\ndirecionava ela através de conversar, perguntar, \\npensar e responder de uma forma de \\nentendimento dos próprios erros, pois a sua \\nfamília tinha sofrido muito, e, com a vida de \\nQuântica, seus avós maternos e paternos guiavam \\nbem os seus filhos em uma direção de vida \\nmelhor, da mesma forma que tiveram, assim os \\npais de Quântica foram bem instruídos a serem \\nuns pais com uma boa conduta de direcionar e \\ncompreender as dificuldades de Quântica.  \\nQuântica, aos 8 anos, tinha a maior média da \\nturma, não tinha uma matéria que ela se \\ndestacava por ter algum dom, e sim uma boa \\ndisciplina familiar, estrutura familiar, o que \\npossibilitava que  ela não tivesse pensamentos \\nruins a pensar e que atrapalhassem o seu",
      "position": 83114,
      "chapter": 1,
      "page": 74,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.42434782608696,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 46.0,
        "avg_word_length": 4.747826086956522,
        "unique_word_ratio": 0.6043478260869565,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.15217391304347827,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "seus",
          "algumas",
          "vida",
          "tinha",
          "anos",
          "sabia",
          "coisas",
          "deixavam",
          "quem",
          "amava",
          "suas",
          "direção",
          "pois",
          "família",
          "pensar",
          "forma",
          "pais",
          "familiar",
          "capítulo"
        ],
        "entities": [
          [
            "1 8",
            "CARDINAL"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "6",
            "DATE"
          ],
          [
            "7",
            "CARDINAL"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "algumas coisas",
            "PERSON"
          ],
          [
            "algumas coisas",
            "PERSON"
          ],
          [
            "algumas pessoas",
            "GPE"
          ],
          [
            "ela \\nadmirava",
            "PERSON"
          ],
          [
            "quem ela \\namava e quem ela não amava",
            "PERSON"
          ]
        ],
        "readability_score": 75.57565217391304,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 139,
        "lexical_diversity": 0.6043478260869565
      },
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "id": 1,
      "text": "crescimento mental e corpóreo, tendo facilidade \\nem um viver com os seus amigos da escola por \\nsempre estar feliz e de bom humor, pois todos os \\ndias, antes de sair de casa, seu pai e sua mãe a \\nbeijavam, abraçavam, falavam que a amavam e \\ndemostravam o amor mais puro ao olhar para a \\nsua filha, Quântica se sentia nas nuvens co m \\naquele aconchego ( acolhimento, amparo físico \\njunto a alguém ou algo; abraço. Ser grato por \\nestar tendo aquele abraço, aquele carinho, sentir \\no sentimento ao tocar. ). \\nQuântica, aos seus 9 anos de idade, já começava a \\nquerer ficar mais com os seus amigos, começando \\na ter um direcionamento dos seus próprios \\namigos, suas vontades, seus desejos, sua conduta, \\nsua importância, seus valores e tudo que um \\nhumano necessita para construir a sua própria \\nvida, pois, naquela idade, o caráter dela já estava \\nformado e di recionado a um caminho, bastava a \\nQuântica ter sabedoria em aprender o seu \\npróprio valor e ambição no meio em que ela já \\nestava vivendo e sendo direcionada, pois sua mãe \\nvirou diretora da empresa e o seu pai virou “dono \\nde casa”, pois o salário que ele gan hava não \\ncompensaria pagar uma empregada, uma babá \\nou alguém que poderia fazer o que ele fazia.  \\nApós completar 10 anos de idade, Quântica viu o \\nseu mundo perfeito desabar.",
      "position": 84583,
      "chapter": 3,
      "page": 75,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.368421052631575,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 45.6,
        "avg_word_length": 4.56140350877193,
        "unique_word_ratio": 0.6403508771929824,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.14035087719298245,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "seus",
          "pois",
          "quântica",
          "amigos",
          "aquele",
          "idade",
          "tendo",
          "casa",
          "mais",
          "alguém",
          "abraço",
          "anos",
          "estava",
          "virou",
          "crescimento",
          "mental",
          "corpóreo",
          "facilidade",
          "viver",
          "escola"
        ],
        "entities": [
          [
            "sempre estar",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "seu pai e sua",
            "ORG"
          ],
          [
            "amor mais puro",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "nas nuvens",
            "PERSON"
          ],
          [
            "amparo físico \\njunto",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "aos",
            "ORG"
          ],
          [
            "9",
            "CARDINAL"
          ]
        ],
        "readability_score": 75.83157894736843,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 146,
        "lexical_diversity": 0.6403508771929824
      },
      "preservation_score": 2.343089548279364e-05
    },
    {
      "id": 1,
      "text": "Sua mãe gostava de dirigir, pois ela acostumou a \\nsempre dirigir indo para o trabalho e, por muitas \\nvezes, no seu próprio trabalho era necessário \\ndirigir, virou costume a sua mãe dirigir, pois sua \\nmãe adquiriu uma habilidade maior que a do seu \\npai. Em um dia comum, sua mãe dirigia, ao lado o \\nseu pai brincava com a Quântica, passean do de \\ncarro sem direção, sem rumo, algo que sua mãe \\ngostava de fazer aos domingos para conversar, \\nolhar as paisagens, distrair, esvaziar a sua mente \\ne ter momentos para aproximar a sua família que, \\ndevido o seu trabalho, faltava tempo. Após 40 \\nminutos com sua família, Quântica e sua família \\nsofreram um acidente de carro, após Quântica \\nlevantar do banco de trás, abraçar a sua mãe \\njunto ao banco do carro e os ombros, sua mãe \\nsentiu um aconchego. Nada em sua vida tinha \\nchegado tão perto daquela energia, pareci a sentir \\na energia do universo (quântico) em seu corpo, \\nfazendo ela se distrair, avançar o sinal vermelho, \\ndesviar de um carro e bater com a lateral do \\nmotorista em um poste, fazendo sua mãe morrer \\ne a Quântica bater com a cabeça fortemente, \\ngerando um coá gulo que a deixou inconsciente \\ncom seu sangue e de sua mãe pelo seu corpo. Seu \\npai, desesperado em ver aquela cena, pois não \\naconteceu nada com ele, saiu sem nenhum \\narranhão, ficou sem reação, só sabia gritar por \\nsocorro e os nomes da esposa e da filha, se us \\npensamentos eram um vazio, sem nada, pois tudo",
      "position": 85995,
      "chapter": 3,
      "page": 76,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.326459143968876,
      "complexity_metrics": {
        "word_count": 257,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 51.4,
        "avg_word_length": 4.4863813229571985,
        "unique_word_ratio": 0.5992217898832685,
        "avg_paragraph_length": 257.0,
        "punctuation_density": 0.14396887159533073,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dirigir",
          "pois",
          "quântica",
          "carro",
          "trabalho",
          "família",
          "nada",
          "gostava",
          "distrair",
          "após",
          "banco",
          "energia",
          "corpo",
          "fazendo",
          "bater",
          "acostumou",
          "sempre",
          "indo",
          "muitas",
          "vezes"
        ],
        "entities": [
          [
            "Sua",
            "PERSON"
          ],
          [
            "ela acostumou",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "dirigir",
            "GPE"
          ],
          [
            "sua mãe dirigia",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "gostava de fazer",
            "PERSON"
          ],
          [
            "aos domingos",
            "PERSON"
          ],
          [
            "para conversar",
            "PERSON"
          ],
          [
            "Após 40",
            "PERSON"
          ]
        ],
        "readability_score": 72.95408560311284,
        "semantic_density": 0,
        "word_count": 257,
        "unique_words": 154,
        "lexical_diversity": 0.5992217898832685
      },
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "id": 1,
      "text": "que ele conquistou na vida estava ali na sua \\nfrente e sem vida...",
      "position": 87549,
      "chapter": 3,
      "page": 77,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.723076923076924,
      "complexity_metrics": {
        "word_count": 13,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 13.0,
        "avg_word_length": 4.076923076923077,
        "unique_word_ratio": 0.9230769230769231,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.23076923076923078,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "conquistou",
          "estava",
          "frente"
        ],
        "entities": [],
        "readability_score": 92.27692307692308,
        "semantic_density": 0,
        "word_count": 13,
        "unique_words": 12,
        "lexical_diversity": 0.9230769230769231
      },
      "preservation_score": 7.231757865059766e-08
    },
    {
      "id": 1,
      "text": "Capítulo 1 9 reviravolta acontece  \\nApós a morte de sua mãe, Quântica e seu pai \\nestavam destruídos mentalmente.  \\nSeu pai não sabia o que fazer, pois o apartamento \\nem que eles moravam era financiado, quem \\npagava as contas da família era a mãe de \\nQuântica, o pai não exercia a profissão há uns 4 \\nanos, não conversava com ninguém do seu \\ntrabalho desde que parou de trabalhar. A vida do \\nseu pai era cuida r da família, organizar os eventos \\nfamiliares, arrumar a casa, cuidar dos avós da \\nQuântica, tanto paterno e materno. O pai de \\nQuântica não tinha tempo para fazer um network , \\nele fazia o melhor para a família em um todo.  \\nQuântica ficou internada no hospital  em coma \\nInduzido por uma semana, após o coma, a \\nQuântica não tinha lembranças de nada do que \\ntinha acontecido, não entendia nem o motivo de \\nestar ali, internada no hospital, com a cabeça \\nenfaixada, o coágulo em sua cabeça, ainda em \\ncicatrização, não permi tia ela assimilar as coisas e \\nnem as pessoas, parecia que ela estava com \\ndislexia ( dificuldade para compreender a leitura, \\napós lesão do sistema nervoso central, \\napresentada por pessoa que anteriormente sabia \\nler). Quântica não sabia que sua mãe estava \\nmorta, o seu pai não sabia como contar e muito \\nmenos falar como o acidente havia ocorrido, pois \\nele sabia que a filha não era culpada, mas se",
      "position": 87768,
      "chapter": 1,
      "page": 78,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.87692307692308,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.0,
        "avg_word_length": 4.589743589743589,
        "unique_word_ratio": 0.6068376068376068,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.12393162393162394,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "sabia",
          "após",
          "família",
          "tinha",
          "fazer",
          "pois",
          "internada",
          "hospital",
          "coma",
          "cabeça",
          "estava",
          "como",
          "capítulo",
          "reviravolta",
          "acontece",
          "morte",
          "estavam",
          "destruídos",
          "mentalmente"
        ],
        "entities": [
          [
            "1 9",
            "DATE"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "Seu",
            "PERSON"
          ],
          [
            "financiado",
            "GPE"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "casa",
            "GPE"
          ],
          [
            "cuidar",
            "NORP"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "Quântica",
            "NORP"
          ]
        ],
        "readability_score": 79.12307692307692,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 142,
        "lexical_diversity": 0.6068376068376068
      },
      "preservation_score": 2.092388608957292e-05
    },
    {
      "id": 1,
      "text": "contasse para a filha a causa do acidente, poderia \\ndestruir a vida dela! O pai de Quântica resolveu \\nguardar esse segr edo para toda a sua vida e não \\ncontou a ninguém.  \\nQuântica, uma semana após acordar do coma, \\nnão parava de perguntar pela mãe, querendo \\nsaber da mãe dela, por muitas vezes, gritava pela \\nmãe, pois não sentia a energia de sua mãe, \\nQuântica, constantemente, ti nha que ser sedada \\npela agitação dela em querer a mãe, o pai de \\nQuântica desesperava -se com tudo que estava \\npassando; o seu irmão e o marido do irmão \\nestavam ao seu lado dia e noite, sempre \\nrevezando entre eles, tentando fazer alguma \\ncoisa em algo impossív el de ser consertado ou \\nmesmo ser aceito, o tio de Quântica, mesmo \\ndesesperado junto com todos da família, era o \\nmais calmo, pois o mesmo tinha passado por \\ndificuldades bem brabas, inclusive uma vez foi \\nparar no hospital por apanhar na rua por ser \\nhomossex ual,  por isso, se sentia mais \\n“confortável” com toda aquela situação, em ser \\nmentalmente mais capaz, devido aos traumas de \\nsua vida serem “normais” no seu dia a dia, ele \\nconversou com o pai de Quântica e ofereceu \\ncontar a verdade para a sua sobrinha, pois  ele já \\nestava com muitos problemas para serem \\nresolvidos, o tio era admirado pela sua sobrinha, \\no respeito que ele tinha sobre ela era \\nproporcional ao respeito pelo o seu próprio pai. O",
      "position": 89223,
      "chapter": 3,
      "page": 79,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.26083333333333,
      "complexity_metrics": {
        "word_count": 240,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 60.0,
        "avg_word_length": 4.55,
        "unique_word_ratio": 0.5958333333333333,
        "avg_paragraph_length": 240.0,
        "punctuation_density": 0.125,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "pela",
          "vida",
          "dela",
          "pois",
          "mesmo",
          "mais",
          "toda",
          "sentia",
          "estava",
          "irmão",
          "tinha",
          "serem",
          "sobrinha",
          "respeito",
          "contasse",
          "filha",
          "causa",
          "acidente",
          "poderia"
        ],
        "entities": [
          [
            "contasse",
            "ORG"
          ],
          [
            "após acordar",
            "PERSON"
          ],
          [
            "gritava pela",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
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
            "noite",
            "GPE"
          ],
          [
            "impossív el de ser",
            "PERSON"
          ],
          [
            "de Quântica",
            "GPE"
          ],
          [
            "todos",
            "NORP"
          ]
        ],
        "readability_score": 68.635,
        "semantic_density": 0,
        "word_count": 240,
        "unique_words": 143,
        "lexical_diversity": 0.5958333333333333
      },
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "id": 1,
      "text": "pai de Quântica, mesmo com tudo que ali estava \\nacontecendo, sabia que  era necessário o seu \\nirmão contar para a sua filha, pois ele já estava \\nsem forças de tanto que vinha apanhando nessas \\nduas semanas, as duas piores semanas as quais \\nele já viveu.  \\nO tio de Quântica entrou em seu quarto com um \\nsorriso triste, logo a Quântica  percebera que \\nvinha uma notícia ruim. Após o coágulo, Quântica \\npercebeu algo diferente com a sua própria \\npessoa, ela percebia os sentimentos das pessoas \\ncom mais facilidade, algo estava diferente, antes \\nmesmo de seu tio contar, ela o abraçou e disse: \\nnão precisa me contar se não quiser, pois eu sei \\nque minha querida mãe morreu.  \\nO tio de Quântica olhou para ela com lágrimas \\nnos olhos, não sabia se era de orgulho junto ao \\nsentimento de dor ou se era a calmaria em si \\npróprio, para ele, esse momento foi quando  ele \\nviu o quanto a sua sobrinha era especial, não só \\npara ele, e sim para o mundo!!!  \\nQuântica olhou para o seu tio e disse: nenhuma \\nmorte é em vão, quando se tem uma vida de \\nexemplo para outros, inclusive para mim, meu tio, \\npois, através de mim, minha mãe  está viva e \\natravés de todos que passaram em sua vida. A \\nmorte é normal para podermos abrir espaço para \\noutras vidas surgirem, pois tudo aquilo que nós \\nfazemos é para melhor nos adaptarmos ao",
      "position": 90702,
      "chapter": 4,
      "page": 80,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.86022408963585,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.666666666666664,
        "avg_word_length": 4.4033613445378155,
        "unique_word_ratio": 0.5882352941176471,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.13445378151260504,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "pois",
          "estava",
          "contar",
          "mesmo",
          "tudo",
          "sabia",
          "vinha",
          "duas",
          "semanas",
          "algo",
          "diferente",
          "disse",
          "minha",
          "olhou",
          "quando",
          "morte",
          "vida",
          "através",
          "acontecendo"
        ],
        "entities": [
          [
            "pai de Quântica",
            "ORG"
          ],
          [
            "ali estava \\nacontecendo",
            "PERSON"
          ],
          [
            "já estava",
            "PERSON"
          ],
          [
            "de Quântica",
            "NORP"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "ela percebia",
            "PERSON"
          ],
          [
            "mesmo de seu",
            "ORG"
          ],
          [
            "ela",
            "PERSON"
          ]
        ],
        "readability_score": 78.84565826330532,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 140,
        "lexical_diversity": 0.5882352941176471
      },
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "id": 1,
      "text": "mundo, sendo assim, a minha mamãe fez algo tão \\ngrande para o mu ndo que, para evoluir o que ela \\nfez, vai ser difícil, pois o amor que ela me mostrou \\nnão se acha com facilidade entre a vida humana, \\npois todos nós somos humanos e não seres \\nhumanos.  \\nO tio da Quântica, assustado por uma menina de \\n10 anos falar sobre a mort e de uma forma tão \\nclara, sentiu medo pela falta de sabedoria em lhe \\ndizer alguma coisa, pois ele foi lá para tentar uma \\nsolução e saiu de lá com a solução.",
      "position": 92138,
      "chapter": 4,
      "page": 81,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.19375,
      "complexity_metrics": {
        "word_count": 96,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 48.0,
        "avg_word_length": 3.9791666666666665,
        "unique_word_ratio": 0.7708333333333334,
        "avg_paragraph_length": 96.0,
        "punctuation_density": 0.11458333333333333,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "humanos",
          "solução",
          "mundo",
          "sendo",
          "assim",
          "minha",
          "mamãe",
          "algo",
          "grande",
          "evoluir",
          "difícil",
          "amor",
          "mostrou",
          "acha",
          "facilidade",
          "entre",
          "vida",
          "humana",
          "todos"
        ],
        "entities": [
          [
            "para evoluir",
            "PERSON"
          ],
          [
            "que ela \\nfez",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "sentiu medo pela",
            "PERSON"
          ],
          [
            "falta de sabedoria",
            "ORG"
          ],
          [
            "para tentar",
            "PERSON"
          ]
        ],
        "readability_score": 74.80625,
        "semantic_density": 0,
        "word_count": 96,
        "unique_words": 74,
        "lexical_diversity": 0.7708333333333334
      },
      "preservation_score": 2.6516445505219144e-06
    },
    {
      "id": 1,
      "text": "Capítulo 20 crescimento no caos  \\nQuântica, com a perda de sua mãe, viu o quanto \\nela havia aprendido com a sua própria mãe, pois \\ncom sua ausência e com o seu acidente, ela sentiu \\na energia do “Quântico” sem perceber. Ela \\ncomeçou a enxergar as coisas como uma forma \\nde aprendizado, eu tive a chance de viver com \\nminha mãe, eu tive a chance de presenciar o am or \\nmais puro do mundo, eu vivi com um exemplo e \\nsei ser exemplo; meu pai, meus avós, meus tios, \\ntodos estão preocupados comigo, pois eu sinto o \\nmeu entorno, vejo que todos pensam: como vai \\nser a Quântica com a morte da mãe dela? E eu \\nentendo que caso do ac aso acontece com todos e \\na graça de um viver é saber que você poder ser o \\nque quiser ser, todos nós sofremos, perdemos, \\nerramos e tudo para um motivo, ser feliz . \\nSe eu for feliz, minha mãe cumpriu a missão de \\nme dar tanto amor e propósito, pois assim será \\ncumprido o propósito que me minha me ensinou a \\nviver desde o início, trabalhando, amando, \\nensinando, sorrindo, abraçando, me sentindo \\ntodas as vezes que eu precisava dela como mãe; e \\nisso que ela me ensinou foi tão bom que eu \\nfazendo isso comigo mesma, eu também serei \\namada e construirei um legado ao mesmo tempo, \\nde importância semelhante ao de minha mãe.  \\nSeu pai e seu tio conversaram sobre o ocorrido e \\nse assustaram com o amadurecimento da",
      "position": 92767,
      "chapter": 20,
      "page": 82,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.278,
      "complexity_metrics": {
        "word_count": 250,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 50.0,
        "avg_word_length": 4.26,
        "unique_word_ratio": 0.612,
        "avg_paragraph_length": 250.0,
        "punctuation_density": 0.132,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "todos",
          "pois",
          "como",
          "viver",
          "quântica",
          "tive",
          "chance",
          "exemplo",
          "meus",
          "comigo",
          "dela",
          "feliz",
          "propósito",
          "ensinou",
          "isso",
          "capítulo",
          "crescimento",
          "caos",
          "perda"
        ],
        "entities": [
          [
            "20",
            "CARDINAL"
          ],
          [
            "quanto \\nela havia aprendido",
            "PERSON"
          ],
          [
            "ela sentiu",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "eu vivi",
            "PERSON"
          ],
          [
            "todos",
            "NORP"
          ],
          [
            "eu sinto o \\nmeu entorno",
            "PERSON"
          ],
          [
            "vejo que",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 73.72200000000001,
        "semantic_density": 0,
        "word_count": 250,
        "unique_words": 153,
        "lexical_diversity": 0.612
      },
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "id": 1,
      "text": "Quântica, começaram a conversar mais com a \\nQuântica sobre a vida, a mbos os lados sempre \\nouvindo e opinando na vida um do outro, sempre \\nno intuito de melhorar, aprimorar, crescer um \\ncom o outro, pois, se você me ama, em quem \\nmais irei confiar? Essa era a nova Quântica para a \\nfamília, porém nunca deixando de ser confiante e  \\ndeterminada para um propósito para todos \\naqueles que ela ama. Sempre que se acontecia \\nalguma adversidade, falta de entendimento, \\nambos os lados perguntavam o motivo de ter \\nfeito ou falado (se nós falamos é porque \\npensamos e, se pensamos, automaticamente e u \\npensei em algo que eu vivi ou estudei), pois todos \\nnós erramos e não podemos ser julgados por um \\nerro ou outro, somos humanos em aprender a \\nsermos seres humanos, sempre estamos \\nevoluindo nossos erros ou até mesmo nossos \\nacertos, pois tudo na vida é um ca minho para um \\naprendizado, se eu não viver em harmonia com \\ntodos, serei mais um que fez guerra na história da \\ncivilização, pois serei mais um humano sendo \\nmelhor que outro humano. Todos pareciam se \\ncompletar na necessidade de se adaptar àquela \\nperda, pois aquilo deu forças para se tornarem \\nmaiores, e esse maior fez Quântica perceber o \\nquanto é necessário viver a vida: o viver de minha \\nmãe foi curto, será que o meu também será?  \\nQuântica percebeu a necessidade de se viver o \\nmelhor em cada idade, com todos aqu eles que \\npassavam em sua vida, ela propagava as regras de",
      "position": 94227,
      "chapter": 4,
      "page": 83,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.37738095238095,
      "complexity_metrics": {
        "word_count": 252,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 50.4,
        "avg_word_length": 4.591269841269841,
        "unique_word_ratio": 0.6190476190476191,
        "avg_paragraph_length": 252.0,
        "punctuation_density": 0.11904761904761904,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "vida",
          "pois",
          "todos",
          "mais",
          "sempre",
          "outro",
          "viver",
          "lados",
          "pensamos",
          "humanos",
          "nossos",
          "serei",
          "humano",
          "melhor",
          "necessidade",
          "será",
          "começaram",
          "conversar",
          "mbos"
        ],
        "entities": [
          [
            "Quântica",
            "ORG"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "nova Quântica",
            "NORP"
          ],
          [
            "deixando de ser",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "se pensamos",
            "PERSON"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós erramos e não podemos ser",
            "FAC"
          ],
          [
            "sempre estamos \\nevoluindo nossos",
            "PERSON"
          ]
        ],
        "readability_score": 73.42261904761905,
        "semantic_density": 0,
        "word_count": 252,
        "unique_words": 156,
        "lexical_diversity": 0.6190476190476191
      },
      "preservation_score": 2.314162516819125e-05
    },
    {
      "id": 1,
      "text": "sua família para todo o seu entorno, limitando, \\nafastando e aproximando quando era necessário. \\nPara estar em minha vida, faça aquilo que você \\nfaria para você, pois eu irei fazer por você o que \\neu qu ero para mim mesma , assim a Quântica foi \\nvivendo as etapas da vida, pois, com essa regra, \\nela se comportava como ela queria ser, sorrindo \\nquando necessário, trabalhando quando \\nnecessário, se divertindo quando necessário, \\nsempre fazendo o necessário e pergu ntando o \\nnecessário a se fazer diante do outro que ali se \\nencontrava, eu sou falha igual a todos, se eu não \\nme motivar, não irei conseguir motivar a \\nninguém , nesse raciocínio, Quântica começava a \\ncrescer e ser mais madura e, no decorrer do seu \\ncrescimento,  ela sentia muitas dores de cabeça, \\ntalvez tenha sido pelo acidente ou por outra coisa \\nque ninguém sabia a razão, pois já se tinha feito \\nmuitos exames e, nos exames, não se detectava \\nnada. Por muitas vezes, a Quântica não conseguia \\nsair do quarto escuro, p ois a enxaqueca que vinha \\na sentir era muito forte, de tal proporção que a \\ndor a fazia inclinar a sua cabeça para baixo e \\nfechar os olhos.  \\nQuântica, por ser uma pessoa simpática e \\nsorridente, por nunca se abalar com os seus \\nproblemas, e sim aprender com os seus \\nproblemas, fez muitos amigos; muitos amigos é \\nsinônimo de fazer muita “merda” e fazer muita \\n“merda” ( felicidade é ser feliz e não  é engraçado;",
      "position": 95783,
      "chapter": 4,
      "page": 84,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.38612244897959,
      "complexity_metrics": {
        "word_count": 245,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 61.25,
        "avg_word_length": 4.6204081632653065,
        "unique_word_ratio": 0.6408163265306123,
        "avg_paragraph_length": 245.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessário",
          "quando",
          "fazer",
          "quântica",
          "você",
          "pois",
          "muitos",
          "vida",
          "irei",
          "motivar",
          "ninguém",
          "muitas",
          "cabeça",
          "exames",
          "seus",
          "problemas",
          "amigos",
          "muita",
          "merda",
          "família"
        ],
        "entities": [
          [
            "sua família",
            "ORG"
          ],
          [
            "quando",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Para estar",
            "PRODUCT"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "pois eu irei fazer",
            "PERSON"
          ],
          [
            "por você o que \\neu qu ero",
            "ORG"
          ],
          [
            "mim mesma",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "essa regra",
            "ORG"
          ]
        ],
        "readability_score": 67.98887755102041,
        "semantic_density": 0,
        "word_count": 245,
        "unique_words": 157,
        "lexical_diversity": 0.6408163265306123
      },
      "preservation_score": 2.796279707823109e-05
    },
    {
      "id": 1,
      "text": "o ser engraçado é trágico vejamos quando \\nalguém cai, erra, machuca, fala besteira, apelidos \\npreconceituosos e tudo aquilo que nos faz rir d a \\n“desgraça” alheia ) é sinônimo de muita felicidade, \\npois a Quântica estava próxima dos seus 17 anos, \\ne os 17 anos têm que ser vividos de acordo com a \\nidade: tenho que viajar com os meus amigos, \\ntalvez beber, se eu tiver responsabilidade, eu \\ntenho que equilibrar a felicidade com a \\nnecessidade, pois como irei fazer algo, se eu não \\nfor responsável com aquilo que  me faz ter esse \\nmesmo algo, eu quero viajar, quero brincar, quero \\nsair, quero subir em árvore, quero andar de skate, \\neu quero viver aquilo que o momento possa me \\nproporcionar de acordo com próprio momento, \\npois eu sei que irei me adaptar e ser feliz.  \\nNess a forma de pensar, a Quântica começou a \\nviver muitas histórias diferentes, escutava \\nhistórias vividas por pessoas diferentes, desde \\nhistórias de felicidade, engraçadas  a histórias \\ntristes; ela escutava, absorvia, estudava, \\nagregava, evoluía e executava, po is, no fim das \\ncontas, ela não poderia brigar com todos, e sim \\nmelhorar um viver posterior, deixando o legado \\nque tinha aprendido com sua mãe.",
      "position": 97307,
      "chapter": 4,
      "page": 85,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.46649746192894,
      "complexity_metrics": {
        "word_count": 197,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 98.5,
        "avg_word_length": 4.888324873096447,
        "unique_word_ratio": 0.649746192893401,
        "avg_paragraph_length": 197.0,
        "punctuation_density": 0.17766497461928935,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quero",
          "histórias",
          "aquilo",
          "felicidade",
          "pois",
          "viver",
          "quântica",
          "anos",
          "acordo",
          "tenho",
          "viajar",
          "irei",
          "algo",
          "momento",
          "diferentes",
          "escutava",
          "engraçado",
          "trágico",
          "vejamos",
          "quando"
        ],
        "entities": [
          [
            "trágico vejamos quando",
            "PERSON"
          ],
          [
            "fala besteira",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "17",
            "CARDINAL"
          ],
          [
            "17",
            "CARDINAL"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "se eu",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "se eu",
            "PERSON"
          ]
        ],
        "readability_score": 49.28350253807107,
        "semantic_density": 0,
        "word_count": 197,
        "unique_words": 128,
        "lexical_diversity": 0.649746192893401
      },
      "preservation_score": 2.1984543909781684e-05
    },
    {
      "id": 1,
      "text": "Capítulo 2 1 sexo, drogas e saber viver  \\nAos 17 anos, Quântica já tinha feitos muitos \\namigos e, com esses amigos, v ieram vivências, \\nacontecimentos, aprendizados, histórias boas e \\nruins e muitas outras coisas que iremos lembrar \\nde acordo com a necessidade do amigo ser falado \\ne lembrado. Quântica, após perder sua mãe, \\nencarou condições financeiras bem ruins, seu pai \\nteve  que vender o apartamento e morar em um \\nlocal “favela bairro”, seu pai estava acostumado a \\nmorar em local em que não havia tiroteio, porém, \\ncom as condições financeiras em que se \\nencontrava não havia outra opção, quando foi à \\nprocura de um emprego, só acho u trabalho, foi \\ntrabalhar consertando computadores em uma \\nloja pequena de informática, com isso, a sua \\nrenda mensal era de um salário mínimo e meio, \\nmas nem tudo foi ruim em sua vida financeira, \\ncom a venda de seu apartamento, deu para quitar \\ne comprar ess a casa bem humilde, assim, o seu \\nsalário dava para dar comida, uma cama, uma \\ntelevisão, suas maquiagens, seu cabelo, roupas \\nadequadas, escola pública e o conforto básico de \\numa vida digna que seu pai vivia.  \\nCom isso, Quântica fez amigos de todas as classes  \\nsociais, de todos os estilos, todas as maluquices. \\nTodas as tribos gostavam da Quântica, pois ela \\nrespeitava o amor que cada um sentia pelo \\npróximo sem ver religião, cor, sexo, aparência e \\nqualquer tipo de preconceito, pois ela antes de",
      "position": 98616,
      "chapter": 2,
      "page": 86,
      "segment_type": "page",
      "themes": {},
      "difficulty": 39.438235294117646,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 59.5,
        "avg_word_length": 4.794117647058823,
        "unique_word_ratio": 0.680672268907563,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.16806722689075632,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "amigos",
          "todas",
          "sexo",
          "ruins",
          "condições",
          "financeiras",
          "apartamento",
          "morar",
          "local",
          "havia",
          "isso",
          "salário",
          "vida",
          "pois",
          "capítulo",
          "drogas",
          "saber",
          "viver",
          "anos"
        ],
        "entities": [
          [
            "Aos 17",
            "LAW"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Quântica",
            "ORG"
          ],
          [
            "após perder sua mãe",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "não havia outra opção",
            "ORG"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "mas nem tudo foi",
            "PERSON"
          ],
          [
            "vida financeira",
            "PERSON"
          ],
          [
            "salário dava para dar comida",
            "PERSON"
          ]
        ],
        "readability_score": 68.81176470588235,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 162,
        "lexical_diversity": 0.680672268907563
      },
      "preservation_score": 2.9360936932142646e-05
    },
    {
      "id": 1,
      "text": "gerar o seu precon ceito, ela perguntava algo \\nreferente ao seu pré-conceito , pois, assim, ela ia \\nentender as respostas que cada um observava \\nperante o seu próprio viver, ela ia vivendo e \\ncompreendendo todos a sua volta, aproximando \\nquem era mais próximo ao seu estilo e afast ando \\ne limitando quem não era próximo a ela, \\nocasionando uma aceitação perante o próprio \\nestilo de vida que sua família a direcionou.  \\nSeus amigos mais próximos eram um casal, \\nhomem e mulher, vindo de uma família de \\ntradição religiosa cristã, de saia longa (Não sei o \\nque a legislação me permite escrever sobre \\nreligião, prefiro não denominar e muito menos \\ndirecionar.), bem conservadores, intuitivos e com \\num direcionamento rígido a um estilo de vida.  \\nQuântica conheceu esse casal  em uma das \\naventuras do casal com os seus amigos \\nhomossexuais, héteros, crianças, avós e muito \\nrespeito um para com o outro.  \\nE nessa viagem dolorida e louca, Quântica \\naprendeu o valor da dieta!  \\nEstava Quântica em um sítio com muitos amigos, \\nsendo várias pessoas diferentes uma das outra s, \\ncom muitas bebidas, vodcas, tequila, gym, cerveja \\ne tudo que poderia misturar para se vomitar. \\nComida, então, puta que pariu , parecia que a \\nQuântica estava fumada com o poder de \\narmazenamento da bolsa da Hermione ou do",
      "position": 100143,
      "chapter": 4,
      "page": 87,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.897873754152826,
      "complexity_metrics": {
        "word_count": 215,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 30.714285714285715,
        "avg_word_length": 4.897674418604651,
        "unique_word_ratio": 0.6604651162790698,
        "avg_paragraph_length": 215.0,
        "punctuation_density": 0.14883720930232558,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "estilo",
          "amigos",
          "casal",
          "perante",
          "próprio",
          "quem",
          "mais",
          "próximo",
          "vida",
          "família",
          "seus",
          "muito",
          "estava",
          "gerar",
          "precon",
          "ceito",
          "perguntava",
          "algo",
          "referente"
        ],
        "entities": [
          [
            "ceito",
            "PERSON"
          ],
          [
            "ela perguntava",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "ela ia",
            "PERSON"
          ],
          [
            "ela ia",
            "PERSON"
          ],
          [
            "quem era mais próximo",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "religiosa cristã",
            "PERSON"
          ],
          [
            "muito menos \\n",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ]
        ],
        "readability_score": 83.17355481727574,
        "semantic_density": 0,
        "word_count": 215,
        "unique_words": 142,
        "lexical_diversity": 0.6604651162790698
      },
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "id": 1,
      "text": "Gato Félix. A variedade de comida,  mais a \\nvariedade de bebida junto ao efeito colateral da \\nmaconha (larica) fizera  a Quântica perceber que \\nos barulhos do nosso estômago são uma sinfonia, \\numa empresa trabalhando igual louca para suprir \\na demanda da quantidade de trabalho.  \\nIrmão, aquele dit ado: quem tem cu tem medo  fez \\ntotal sentido para Quântica.  \\nPensa: lembrarei apenas algumas das coisas que a \\nQuântica consumiu, pois, em alguns momentos, \\ndevido ao consumo, ela não lembrará o que ela \\nmesmo consumiu, ficando 4 dias no sítio, sendo \\nos dias de  quinta a domingo; e, no meio desses \\ndias, era o ano novo.  \\nQuinta -feira: estrogonofe de frango, refrigerante, \\ncerveja, churrasco, pão com várias coisas dentro, \\ncafé, água (raramente), cerveja, churrasco (não é \\nreplay  da mesma palavra, isso foi contínuo, to dos \\nos tipos de carne e algumas eu não sei dizer de \\nqual animal provinha). Quântica teve uma falha \\nno sistema, a fazendo agir como no automático \\ndo Click , fazendo ela comer e beber sem \\nperceber.  \\nDomingo: pão com ovo, pão com queijo e \\npresunto, rabanada, qu ibe, batata frita com \\ncream cheese  e bacon, cebola empanada, tábua \\nde frios, feijoada e churrasco; isso foi só a comida \\nque ela ingeriu, fora a bebida que estava do \\nmesmo jeito de quinta -feira. Domingo, a Quântica",
      "position": 101559,
      "chapter": 4,
      "page": 88,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.08233944954128,
      "complexity_metrics": {
        "word_count": 218,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.25,
        "avg_word_length": 4.8577981651376145,
        "unique_word_ratio": 0.7110091743119266,
        "avg_paragraph_length": 218.0,
        "punctuation_density": 0.20642201834862386,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "dias",
          "quinta",
          "domingo",
          "churrasco",
          "variedade",
          "comida",
          "bebida",
          "perceber",
          "algumas",
          "coisas",
          "consumiu",
          "mesmo",
          "feira",
          "cerveja",
          "isso",
          "fazendo",
          "gato",
          "félix",
          "mais"
        ],
        "entities": [
          [
            "Gato Félix",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "medo",
            "GPE"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "ela não lembrará o",
            "PERSON"
          ],
          [
            "ela \\nmesmo consumiu",
            "PERSON"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "ano novo",
            "ORG"
          ],
          [
            "Quinta",
            "PERSON"
          ]
        ],
        "readability_score": 84.91766055045872,
        "semantic_density": 0,
        "word_count": 218,
        "unique_words": 155,
        "lexical_diversity": 0.7110091743119266
      },
      "preservation_score": 3.577309557249564e-05
    },
    {
      "id": 1,
      "text": "já estava exausta, porém estava firme e fo rte com \\nos seus amigos.  \\nAo ir ao banheiro, Quântica percebeu que a \\nquantidade de coisas ingeridas fez o corpo entrar \\nem um colapso quântico de distribuição de \\nvalores calóricos e vitaminas de A a zinco, sem \\norganização e com muito barulho, sendo que \\ntudo n o corpo de Quântica estava se mexendo e \\ntudo fazia barulho trabalhando.  \\nUm grupo de homossexuais, lésbica, gay, viado, \\nsimpatizante, travesti e o símbolo + da bandeira, \\ntodos os tipos de humanos estavam presentes — \\neu não entendo qual é a diferença de um p ara o \\noutro, pois até o lutar contra o preconceito se \\ntorna perigoso, preconceituoso, extremista e \\nmuitas outras coisas que ocorreram em vários \\noutros movimentos que foram além do \\nnecessário para se ter liberdade e não regrar um \\nviver de alguém, hoje eu ve jo que conquistamos \\nmuitos direitos, temos internet, câmera em todos \\nos lugares e qualquer coisa que eu vejo na \\ntelevisão, que eu leio na história da humanidade \\ntem mais histórias de caos do que amor e \\nfelicidade, assim fomos moldando a nossa \\nexistência e a nossa adaptação um para com o \\noutro, a necessidade de se ter regras é visível, \\nporém, a necessidade de não se ter regras \\ntambém é visível, o problema das regras não são \\nas regras ou o excesso delas, pois o problema das \\nregras está em quem as interpreta.",
      "position": 102989,
      "chapter": 4,
      "page": 89,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 38.38559322033898,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 78.66666666666667,
        "avg_word_length": 4.61864406779661,
        "unique_word_ratio": 0.6228813559322034,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.11016949152542373,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "regras",
          "estava",
          "porém",
          "quântica",
          "coisas",
          "corpo",
          "barulho",
          "tudo",
          "todos",
          "outro",
          "pois",
          "nossa",
          "necessidade",
          "visível",
          "problema",
          "exausta",
          "firme",
          "seus",
          "amigos",
          "banheiro"
        ],
        "entities": [
          [
            "já estava exausta",
            "PERSON"
          ],
          [
            "porém estava",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "calóricos",
            "NORP"
          ],
          [
            "vitaminas de A",
            "ORG"
          ],
          [
            "muito barulho",
            "PERSON"
          ],
          [
            "mexendo e \\ntudo fazia barulho trabalhando",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "eu não entendo",
            "PERSON"
          ],
          [
            "pois até o lutar contra",
            "ORG"
          ]
        ],
        "readability_score": 59.28107344632768,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 147,
        "lexical_diversity": 0.6228813559322034
      },
      "preservation_score": 1.8874888027805986e-05
    },
    {
      "id": 1,
      "text": "Esse amigo é o mais inteligente e o mais \\nengraçado, ele era um anão com cabelo rastafári \\ne a cor dele era quase azul, de tão preto, andava \\nde skate, não fumava maconha e os seus pais \\nmoravam na maior casa que a Quântica já tinha \\nvisto. Após ele descobrir q ue a Quântica tinha \\nusado drogas, bebido, fumado maconha, ele foi \\nconversar com ela sobre os benefícios e os \\nmalefícios das drogas, pois ele usava bala, doce e \\nMD, tudo dentro de uma dosagem, pois, assim \\ncomo ela errou em usar em uma  escala \\nexagerada, ele também já tinha cometido esses  \\nexcessos  algumas vezes, o fazendo perceber até \\nque ponto ele poderia consumir e ser usuário, o \\nmaior medo dele em ser usuário era se \\ntransformar em viciado, então ele, sendo \\nestudioso, começou a estudar os efeitos das \\ndrogas teoricamente, para saber qual é menos o u \\nmais fácil de controlar, até porque ele é a favor \\nde viver a vida dentro de uma regra de viver o \\nmelhor em um contexto, ele sofria muito com a \\ndiscriminação visual, racial, tamanho e muitas \\noutras formas de julgamento. Ele não desejava as \\ncoisas que ele viveu para ninguém, porém o \\njulgamento dos outros não poderia direcionar a \\nsua felicidade em usar aquela droga de uma \\nforma controlada. Conversando com a Quântica, \\nele pegou uma bala e dividiu em 3 partes, tomou \\num terço, enquanto ele esperava a droga faze r \\nefeito, ele ficou conversando com a Quântica \\nsobre drogas, a ensinando a abrir a mente,",
      "position": 104462,
      "chapter": 4,
      "page": 90,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.361176470588234,
      "complexity_metrics": {
        "word_count": 255,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 63.75,
        "avg_word_length": 4.537254901960784,
        "unique_word_ratio": 0.6313725490196078,
        "avg_paragraph_length": 255.0,
        "punctuation_density": 0.12941176470588237,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "drogas",
          "mais",
          "tinha",
          "dele",
          "maconha",
          "maior",
          "pois",
          "bala",
          "dentro",
          "usar",
          "poderia",
          "usuário",
          "viver",
          "julgamento",
          "droga",
          "conversando",
          "esse",
          "amigo",
          "inteligente"
        ],
        "entities": [
          [
            "engraçado",
            "GPE"
          ],
          [
            "cor",
            "ORG"
          ],
          [
            "andava \\nde skate",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Após ele descobrir",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "ela sobre",
            "PERSON"
          ],
          [
            "ele usava bala",
            "PERSON"
          ],
          [
            "MD",
            "GPE"
          ],
          [
            "dentro de uma dosagem",
            "ORG"
          ]
        ],
        "readability_score": 66.76382352941177,
        "semantic_density": 0,
        "word_count": 255,
        "unique_words": 161,
        "lexical_diversity": 0.6313725490196078
      },
      "preservation_score": 2.3864800954697227e-05
    },
    {
      "id": 1,
      "text": "opinião, limitar, efeitos... A Quântica, assustada \\npela tranquilidade que ele apresentava, \\nperguntou para o amigo: o que você acha da \\nmaconha?  \\nEle respondeu para ela:  é uma droga legal de se \\nusar quando se sabe usar, tudo em nosso mundo \\nfaz mal para o nosso corpo se não souber usar, as \\nque mais causam malefícios ao nosso corpo são \\nas drogas liberadas. A maconha dá a sensação de \\nconforto, porém algumas pessoas que já tê m um \\npensamento mais devagar, quando fuma, fica \\ncom o pensamento mais devagar ainda, \\ntransformando -se em uma pessoa sem atenção \\nao seu entorno e ficando só na onda. Óbvio que \\ntêm pessoas que precisam fumar em vez de \\ntomar até um relaxante, calmante, remédi o para \\ndormir ou, se a pessoa é hiperativa, a maconha a \\ndeixa mais estável, não é a cura, e sim \\nestabilidade com a situação, ela dá sensação de \\nconforto, porém na nossa idade não é \\naconselhável fumar maconha, na nossa idade, nós \\ntemos que nos estimular a v iver e não sentir \\nconforto na vida, pois como iremos criar vontade \\npara trabalhar? Vontade de ter uma família? \\nVontade de ter uma vida digna? O sentir conforto \\né estagnar ( fazer parar ou parar de fluir; estancar. \\nfazer cessar ou cessar o progresso ou o \\nfuncionamento; paralisar ) a sua vida e como a \\nnossa origem, como você mesma me ensinou, \\nveio através do movimento, o se movimentar é",
      "position": 106022,
      "chapter": 4,
      "page": 91,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.642212924221294,
      "complexity_metrics": {
        "word_count": 239,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 26.555555555555557,
        "avg_word_length": 4.548117154811716,
        "unique_word_ratio": 0.6192468619246861,
        "avg_paragraph_length": 239.0,
        "punctuation_density": 0.1589958158995816,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "maconha",
          "mais",
          "conforto",
          "usar",
          "nosso",
          "nossa",
          "vida",
          "como",
          "vontade",
          "você",
          "quando",
          "corpo",
          "sensação",
          "porém",
          "pessoas",
          "pensamento",
          "devagar",
          "pessoa",
          "fumar",
          "idade"
        ],
        "entities": [
          [
            "limitar",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "assustada",
            "GPE"
          ],
          [
            "para ela",
            "PERSON"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "mal para",
            "PRODUCT"
          ],
          [
            "drogas liberadas",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "fica",
            "GPE"
          ]
        ],
        "readability_score": 85.3577870757787,
        "semantic_density": 0,
        "word_count": 239,
        "unique_words": 148,
        "lexical_diversity": 0.6192468619246861
      },
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "id": 1,
      "text": "necessário para ter um corpo saudável, exercitar \\na saúde mental é necessário para se manter \\nlúcido, tudo em nossa vida é movim entar, o \\nestagnar é a morte da nossa própria energia.  \\nHavia o grupo das amigas da escola; nesse grupo, \\na que mais se destacava pela beleza e por ter \\nmais dinheiro era a maconheira do grupo, ela \\nestudava ali porque o seu pai e sua mãe não \\naguentavam mais pa gar escola e ela matar aula \\npara fumar maconha, os pais toda hora \\nprecisavam ir até a escola, repetiu de ano duas \\nvezes e bebia todos os finais de semana com os \\namigos mais velhos, pois eles tinham carros e \\nbancavam ela. Após alguns anos, a família dela \\ndesistiu de dar qualquer tipo de ajuda financeira, \\npois entenderam que dar dinheiro era sustentar a \\nvida confortável dela, logo após isso acontecer, \\nela foi trabalhar de secretária em um escritório de \\nadvocacia, não durou muito tempo, pois não \\nconseguia se c oncentrar no trabalho, sempre \\nestava com a mente acelerada e fragmentada \\ndevido ao uso contínuo da maconha, tornando -a \\ndependente devido ao excesso de uso, fazendo o \\nseu cérebro virar escravo da maconha. Não \\nconseguindo usar em horário de expediente, ela \\ncomeçou a compensar a ausência do dia para o \\nhorário de seu descanso com maconha e álcool, \\npois não conseguia se encaixar no seu trabalho, \\nlevando -a a ter fugas com drogas mais pesadas,",
      "position": 107494,
      "chapter": 4,
      "page": 92,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.39620253164557,
      "complexity_metrics": {
        "word_count": 237,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 59.25,
        "avg_word_length": 4.654008438818566,
        "unique_word_ratio": 0.6540084388185654,
        "avg_paragraph_length": 237.0,
        "punctuation_density": 0.10548523206751055,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "maconha",
          "pois",
          "grupo",
          "escola",
          "necessário",
          "nossa",
          "vida",
          "dinheiro",
          "após",
          "dela",
          "conseguia",
          "trabalho",
          "devido",
          "horário",
          "corpo",
          "saudável",
          "exercitar",
          "saúde",
          "mental"
        ],
        "entities": [
          [
            "necessário",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Havia",
            "NORP"
          ],
          [
            "grupo",
            "ORG"
          ],
          [
            "das amigas da escola",
            "PRODUCT"
          ],
          [
            "se destacava pela",
            "PERSON"
          ],
          [
            "ela \\nestudava",
            "PERSON"
          ],
          [
            "ela matar aula \\n",
            "PERSON"
          ],
          [
            "para fumar maconha",
            "PERSON"
          ],
          [
            "toda hora",
            "PERSON"
          ]
        ],
        "readability_score": 68.97879746835443,
        "semantic_density": 0,
        "word_count": 237,
        "unique_words": 155,
        "lexical_diversity": 0.6540084388185654
      },
      "preservation_score": 1.822402981995061e-05
    },
    {
      "id": 1,
      "text": "devido a sua própria falha de não perceber os \\nseus excessos pela imatur idade.  \\n Havia, ainda, a galera que complementava essa \\nbagunça: os estudiosos, nerds, bagunceiros, \\nfazedores de merda, bandidinhos e muitos outros \\nque não lembrarei, mas, se eu recordar, \\nescreverei no decorrer do livro.  \\nPróximo à sua casa, por muitas vezes,  \\naconteceram alguns tiroteios, algumas mortes e, \\naos 17 anos, conheceu  uma pessoa através da sua \\namiga maconheira, a mesma, por si só, o \\nconheceu na boca de fumo ao ir comprar \\nmaconha, Quântica perguntou para ele por qual \\nmotivo estava vivendo aquela vida . \\nQuântica, eu fui criado por uma mãe que era \\nusuária de crack, todas as vezes que eu tentava ir \\npara escola, ela me trazia para o mundo dela, \\nalegando que, se eu não a ajudasse, ela ia morrer \\nde fome, pois eu era o sustento, meu e dela, para \\ntermos comida . Eu, sendo criança, não sabia \\ncomo fazer, pois quando eu pedia dinheiro nos \\ncarros, as pessoas me olhavam com um olhar de \\n“medo”, eu não tinha muitas escolhas em minha \\nvida, tive que fazer minhas correrias do jeito que \\ndava.  \\nAquelas palavras a comoveram, ela começou a \\nsondar com os amigos dela, se alguém sabia \\ncomo arrumar um emprego para aquele jovem. Já \\nera tarde para arrumar um emprego para o rapaz,",
      "position": 108978,
      "chapter": 4,
      "page": 93,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.971883116883117,
      "complexity_metrics": {
        "word_count": 220,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 31.428571428571427,
        "avg_word_length": 4.668181818181818,
        "unique_word_ratio": 0.7,
        "avg_paragraph_length": 220.0,
        "punctuation_density": 0.19545454545454546,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dela",
          "muitas",
          "vezes",
          "conheceu",
          "quântica",
          "vida",
          "pois",
          "sabia",
          "como",
          "fazer",
          "arrumar",
          "emprego",
          "devido",
          "própria",
          "falha",
          "perceber",
          "seus",
          "excessos",
          "pela",
          "imatur"
        ],
        "entities": [
          [
            "devido a sua própria",
            "PERSON"
          ],
          [
            "de não perceber os",
            "ORG"
          ],
          [
            "Havia",
            "GPE"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "essa \\nbagunça",
            "ORG"
          ],
          [
            "bagunceiros",
            "GPE"
          ],
          [
            "se eu recordar",
            "PERSON"
          ],
          [
            "Próximo",
            "PERSON"
          ],
          [
            "17",
            "CARDINAL"
          ],
          [
            "amiga maconheira",
            "PERSON"
          ]
        ],
        "readability_score": 82.88525974025974,
        "semantic_density": 0,
        "word_count": 220,
        "unique_words": 154,
        "lexical_diversity": 0.7
      },
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "id": 1,
      "text": "pois esse emprego que ela arrumaria de nada \\nadiantava, já que, naquela tarde, ele veio a tomar \\num tiro e ficou paraplégico, e o trabalho que ela \\ntinha arrumado era de lavador de carros. Após ele \\ntomar tiro e ficar paraplégico, ainda foi preso, \\npegando 10 anos de cadeia. Na cadeia, ele entrou \\npara um grupo religioso que o fez enxergar outros \\ncaminhos, o ensina ram a ler e escrever, com \\ngrupos de apoio na cadeia, ele virou atleta de \\nlevantamento de peso paraolímpico, a que, no \\ndecorrer de sua vida, se dedicou inteiramente, o \\nfazendo conhecer sua esposa e ter dois filhos.  \\nAinda com os seus 17 anos, Quântica teve s ua \\nprimeira relação sexual, mas, em sua vida, \\nQuântica nunca escolheu homem ou mulher, ela \\nsempre beijou quem ela se sentia à vontade em \\nbeijar, fosse mulher ou  homem, ela não se \\nimportava, pois ela sentia a energia da pessoa, ao \\nse aproximar, olhar nos ol hos, tocar, conversar, e, \\nse ela se sentisse à vontade para beijar, ela \\nbeijava, pois ela amava o sentimento bom de se \\napaixonar pelo o outro.  \\nQuântica perdeu a sua virgindade com um \\nhomem com um pênis de 20cm, ela, por nunca \\nter feito sexo antes, não sabi a como se comportar \\ne nem falar sobre algo que o seu ginecologista a \\nalertava: o seu útero baixo comprimia a sua \\npassagem, quando ela fosse ter relações era \\nnecessário usar uma pomada lubrificante para a \\npenetração não ser tão agressiva. Quântica não",
      "position": 110374,
      "chapter": 4,
      "page": 94,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.36746987951807,
      "complexity_metrics": {
        "word_count": 249,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.5,
        "avg_word_length": 4.5582329317269075,
        "unique_word_ratio": 0.6385542168674698,
        "avg_paragraph_length": 249.0,
        "punctuation_density": 0.1606425702811245,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "pois",
          "cadeia",
          "homem",
          "tomar",
          "tiro",
          "paraplégico",
          "ainda",
          "anos",
          "vida",
          "nunca",
          "mulher",
          "sentia",
          "vontade",
          "beijar",
          "fosse",
          "esse",
          "emprego",
          "arrumaria",
          "nada"
        ],
        "entities": [
          [
            "ela arrumaria de nada \\nadiantava",
            "PERSON"
          ],
          [
            "naquela tarde",
            "PERSON"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "paraplégico",
            "ORG"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "foi preso",
            "PERSON"
          ],
          [
            "10",
            "CARDINAL"
          ],
          [
            "fez enxergar outros \\ncaminhos",
            "ORG"
          ],
          [
            "ensina ram",
            "ORG"
          ],
          [
            "virou atleta de \\nlevantamento de peso",
            "PERSON"
          ]
        ],
        "readability_score": 77.88253012048193,
        "semantic_density": 0,
        "word_count": 249,
        "unique_words": 159,
        "lexical_diversity": 0.6385542168674698
      },
      "preservation_score": 2.796279707823109e-05
    },
    {
      "id": 1,
      "text": "tinha  pomada e já estava pelada, devido a \\nemoção do momento. resolveu continuar, pois \\nela também tinha curiosidade e gostava do rapaz \\ncomo amigo, não como namorado. Quântica, ao \\nser penetrada, sentiu uma dor que nunca havia \\nsentido antes, nem as suas dores de c abeça eram \\ntão fortes quanto essa que ela estava sentindo, \\nela, por sua vez, estava ficando muito \\nincomodada com aquilo, estava se sentindo \\ninvadida, mas, por  ser inexperiente, não sabia que \\naquela situação era anormal, ela aguentou esse \\nincômodo até o fin al e, após o término daquele \\nato sadomasoquista, ela não queria que o rapaz a \\nencostasse, ela sentia repúdio por ele, que, por \\nsua vez, não estava entendendo, pois ele a amava \\ne queria conquistar a Quântica para viver uma \\nvida ao seu lado, até porque ele s onhava em \\nperder a virgindade com a mulher que ele ia \\ncasar, no entanto, Quântica, sem saber o motivo, \\nsó queria se afastar do rapaz. Posteriormente, \\nQuântica ia descobrir que o real motivo daquela \\nrepelência, foi adquirido através do excesso de \\ndor sentid o no ato, essa dor a qual ela sentiu foi \\nsemelhante a sensação de ter sido estuprada, por \\nela não estar mais com vontade.",
      "position": 111905,
      "chapter": 4,
      "page": 95,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.415346534653466,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 50.5,
        "avg_word_length": 4.717821782178218,
        "unique_word_ratio": 0.6633663366336634,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.16831683168316833,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estava",
          "quântica",
          "rapaz",
          "queria",
          "tinha",
          "pois",
          "como",
          "sentiu",
          "essa",
          "sentindo",
          "motivo",
          "pomada",
          "pelada",
          "devido",
          "emoção",
          "momento",
          "resolveu",
          "continuar",
          "também",
          "curiosidade"
        ],
        "entities": [
          [
            "pomada",
            "GPE"
          ],
          [
            "já estava",
            "PERSON"
          ],
          [
            "resolveu",
            "PERSON"
          ],
          [
            "ela também",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "sentido antes",
            "PERSON"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "quanto essa",
            "PERSON"
          ],
          [
            "ela estava sentindo",
            "PERSON"
          ],
          [
            "por sua vez",
            "ORG"
          ]
        ],
        "readability_score": 73.33465346534653,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 134,
        "lexical_diversity": 0.6633663366336634
      },
      "preservation_score": 1.967038139296256e-05
    },
    {
      "id": 1,
      "text": "Capítulo 2 2 sabedoria no caos  \\nQuântica, por muitas vezes, ignorou o seu poder \\nde intuição de sentir medo por estar errada, por \\nmedo de  agir incorretamente e, frequentemente, \\nisso fez mal somente para ela. Aos seus 25 anos, \\nQuântica já estava trabalhando em uma empresa \\nde publicidade que fazia comerciais para \\ntelevisão, Quântica se destacava pela sua energia, \\nempatia, companheirismo, empe nho, dedicação. \\nNessa empresa, ela entrou como secretária, \\nsendo uma secretária, se destacou em sua forma \\nde se comunicar, logo uma produtora viu a \\nsagacidade, criatividade, feeling , epifanias que a \\nQuântica tinha, percebeu que aquela menina \\ntinha algo esp ecial, algo diferente que ela só \\nsentia e podia confiar no seu instinto, foi o que \\nela fez, trazendo a Quântica para a parte da \\ncriatividade, assim que a Quântica foi chamada \\npara a parte da criatividade da empresa, era para \\nobservar e aprender. Na primeir a reunião que a \\nQuântica participava ao lado da produtora para \\nobservar as anotações ou ajudar nas anotações, \\nela observou que as falas do comercial, junto a \\nfotografia não passavam o sentimento necessário, \\npois, dependendo de qual humano assistisse \\naquele  comercial, iria interpretar de uma forma \\ntotalmente oposta à mensagem a ser passada \\npelo comercial. A produtora se assustou com o \\nargumento que a Quântica tinha usado para \\nexplicar sobre o comercial, tinha falado com",
      "position": 113210,
      "chapter": 2,
      "page": 96,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.557847533632284,
      "complexity_metrics": {
        "word_count": 223,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 44.6,
        "avg_word_length": 5.192825112107624,
        "unique_word_ratio": 0.6547085201793722,
        "avg_paragraph_length": 223.0,
        "punctuation_density": 0.15246636771300448,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "tinha",
          "comercial",
          "empresa",
          "produtora",
          "criatividade",
          "medo",
          "secretária",
          "forma",
          "algo",
          "parte",
          "observar",
          "anotações",
          "capítulo",
          "sabedoria",
          "caos",
          "muitas",
          "vezes",
          "ignorou",
          "poder"
        ],
        "entities": [
          [
            "2 2",
            "CARDINAL"
          ],
          [
            "ignorou",
            "PERSON"
          ],
          [
            "medo por estar errada",
            "PERSON"
          ],
          [
            "medo de  agir",
            "PERSON"
          ],
          [
            "para ela",
            "PERSON"
          ],
          [
            "Aos",
            "PERSON"
          ],
          [
            "25",
            "CARDINAL"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "já estava trabalhando",
            "PERSON"
          ],
          [
            "para \\ntelevisão",
            "PERSON"
          ]
        ],
        "readability_score": 76.14215246636772,
        "semantic_density": 0,
        "word_count": 223,
        "unique_words": 146,
        "lexical_diversity": 0.6547085201793722
      },
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "id": 1,
      "text": "muito detalhe sobre os erros e os moti vos \\nsentimentais envolvidos, sobre a mensagem que \\no contratante queria passar e o alcance \\nsentimental do seu produto para a família \\nbrasileira.  \\nAo se destacar por falar o que vinha a sentir, \\nQuântica resolveu seguir o seu instinto pelo resto \\nda vida, até p orque ela, sem ter feito faculdade, \\ncom todos os problemas que tinha passado em \\num viver,  tornou -se diretora na parte de \\ncriatividade dos comerciais aos seus 27 anos, sem \\nfaculdade e com apenas sua dedicação e \\ndeterminação, ela conseguiu se destacar por v iver \\ne fazer o melhor que ela poderia em qualquer \\nsituação que surgia para ela viver, pois o nosso \\npassado é o aprendizado para vivermos um futuro \\nmelhor e o presente, como diz o próprio nome, já \\nsabemos o significado de estarmos vivos, pois o \\nestar vivo é  um presente!  \\nQuântica decidiu dedicar a sua vida, seu \\naprendizado, sua captação de energia, seus \\ninstintos em segui -los e fazer deles o melhor \\nexemplo que ela poderia, pois todos que estão \\nvivos são um presente da vida, se são um \\npresente da vida, merecem  viver a vida!  \\nInfelizmente, tem vidas que, devido a própria \\nvida, não conseguimos direcionar, e vidas que \\ntomam uma direção que não querem voltar, todos \\nnós temos que aprender a admirar o presente,",
      "position": 114738,
      "chapter": 4,
      "page": 97,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 37.409459459459455,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.5,
        "avg_word_length": 4.698198198198198,
        "unique_word_ratio": 0.6261261261261262,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.12162162162162163,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "presente",
          "todos",
          "viver",
          "melhor",
          "pois",
          "destacar",
          "quântica",
          "faculdade",
          "passado",
          "seus",
          "fazer",
          "poderia",
          "aprendizado",
          "vivos",
          "vidas",
          "muito",
          "detalhe",
          "erros",
          "moti"
        ],
        "entities": [
          [
            "muito detalhe",
            "PERSON"
          ],
          [
            "moti",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "até p",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "aos",
            "ORG"
          ],
          [
            "27",
            "CARDINAL"
          ],
          [
            "apenas sua dedicação",
            "ORG"
          ]
        ],
        "readability_score": 70.84054054054054,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 139,
        "lexical_diversity": 0.6261261261261262
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "pois ele foi construído através de seu passado, e \\nessa co nstrução é uma conquista impagável, seja \\nfeliz e confiante, pois eu sei que farei o melhor \\nque eu posso para todos aqueles que passarem \\nem minha vida, irei conversar se necessário, \\nescutar se for necessário, abraçar se for \\nnecessário, olhar se for necessár io, sentir se for \\nnecessário e, o principal, irei conquistar e amar \\ntodos aqueles que forem o mesmo comigo, sem \\ndeixar de fazer sexo quando e com quem eu \\nquiser, sem deixar de trabalhar e fazer o meu \\nmelhor para poder conquistar o meu melhor, sem \\ndeixar de  beber bebida alcoólica, fumar maconha \\ne usar qualquer droga que eu saiba que serei uma \\nusuária nos meus momentos de felicidade, nos \\nmomentos certos, com pessoas certas, com a \\ndosagem certa. A partir de agora, irei trabalhar \\npara viver e não viver para o t rabalho, pois eu \\ntenho tempo para viajar e sair, tenho uma casa \\nsatisfatória, tenho um carro, tenho meu salário e \\na minha carreira, é só eu fazer o que eu preciso \\nfazer, irei viver o melhor da vida, pois conquistei a \\nminha liberdade em um conforto de viver  a minha \\nprópria vida.  \\nUm belo dia, estava Quântica com uma dúvida \\nsobre o trabalho, foi até a sala da produtora \\namiga e conselheira tirar essa  dúvida, quando de \\nrepente ela olhou para a sua amiga, viu sua amiga \\ncom uma calculadora e uma pilha de folha A4,  ela \\nfoleava e digitava os números na calculadora,",
      "position": 116152,
      "chapter": 4,
      "page": 98,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.505976095617534,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 83.66666666666667,
        "avg_word_length": 4.54183266932271,
        "unique_word_ratio": 0.5657370517928287,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.13147410358565736,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "melhor",
          "minha",
          "irei",
          "necessário",
          "fazer",
          "viver",
          "tenho",
          "vida",
          "deixar",
          "amiga",
          "essa",
          "todos",
          "aqueles",
          "conquistar",
          "quando",
          "trabalhar",
          "momentos",
          "dúvida",
          "calculadora"
        ],
        "entities": [
          [
            "eu",
            "PERSON"
          ],
          [
            "que eu posso",
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
            "abraçar se",
            "PERSON"
          ],
          [
            "forem o",
            "ORG"
          ],
          [
            "mesmo comigo",
            "ORG"
          ],
          [
            "deixar de fazer",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "quem eu \\nquiser",
            "PERSON"
          ]
        ],
        "readability_score": 56.80411686586985,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 142,
        "lexical_diversity": 0.5657370517928287
      },
      "preservation_score": 2.306930758954065e-05
    },
    {
      "id": 1,
      "text": "somando uma atrás da outra. Quântica curiosa \\nperguntou: você sabe o quanto de dinheiro você \\ntem?  \\nSua amiga olhou nos olhos de Quântica e \\nrespondeu: Quântica, o valor do humano é o valor \\nda dívida dele.  \\nQuântica percebeu, então, que as aparências são \\nvistas de acordo com a necessidade imposta pelo \\nseus próprios sonhos e desejos, pois a resposta \\nfoi mais adiante e a produtora explicou por qual \\nmotivo foi dada essa resposta.  \\nQuântica, hoje eu estou com o saldo  negativo de \\nR$280.000,00 porém ainda tenho que pagar \\nR$450.000,00, mas esses R$450.000,00 são para \\nempresas que eu já trabalho há muito tempo, são \\nempresas que eu tenho credibilidade, crédito, \\nconfiança, pois eles sabem que eu não deixo de \\npagar, e como e u sei que pagarei? Eu sei que \\ntemos que fazer esses comerciais, mas esses \\ncomerciais ainda vão ser editados, conferidos, \\naprovados pelo contratante. Eu sei que temos em \\ntorno de R$ 1,500.000,00 a receber e mais um \\ncusto futuro de R$ 320.000,00; temos um lu cro \\nprevisto de R$ 450.000,00, pois temos que fazer \\ncaixa e, se não fizermos caixa, trabalharemos sob \\npressão, com preocupação, nervosos e isso, para \\nqualquer empresa, não é lucrativo.  \\nQuântica, sempre muito sentimental, ficou \\npensando em várias coisas atr avés desse",
      "position": 117692,
      "chapter": 4,
      "page": 99,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.135645604395606,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 14.857142857142858,
        "avg_word_length": 4.975961538461538,
        "unique_word_ratio": 0.6682692307692307,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.22115384615384615,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "temos",
          "pois",
          "esses",
          "você",
          "valor",
          "pelo",
          "resposta",
          "mais",
          "ainda",
          "tenho",
          "pagar",
          "empresas",
          "muito",
          "fazer",
          "comerciais",
          "caixa",
          "somando",
          "atrás",
          "outra"
        ],
        "entities": [
          [
            "somando uma atrás da outra",
            "ORG"
          ],
          [
            "quanto de dinheiro",
            "ORG"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "Quântica",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "vistas de acordo",
            "ORG"
          ],
          [
            "foi mais adiante",
            "PERSON"
          ],
          [
            "dada essa resposta",
            "ORG"
          ],
          [
            "hoje eu",
            "PERSON"
          ],
          [
            "para \\nempresas",
            "ORG"
          ]
        ],
        "readability_score": 91.0786401098901,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 139,
        "lexical_diversity": 0.6682692307692307
      },
      "preservation_score": 3.104834710065659e-05
    },
    {
      "id": 1,
      "text": "raciocínio que a produtora teve; na vida dela, o \\nquanto se encaixava esse pensamento diante de \\num viver, Quântica começou a perceber que a \\nvida é uma troca, nós só temos aquilo \\nproporcional ao que fazemos, se não fazemos, \\nnão conseguimos gerar o portunidade para se ter \\noportunidade, não se tendo oportunidade, se \\nacaba a dívida. Quântica percebeu que até o \\nsentimento tem um valor de dívida perante o \\noutro, pois o casamento é um acordo, e, sendo \\num acordo, eu tenho que cumprir com o meu \\nacordo. Agor a, se eu caso e faço um acordo com o \\nmeu cônjuge de irmos para a suruba, orgia, \\nménage , eu estou de acordo com a dívida \\nsentimental que eu combinei com a pessoa que \\nestá comigo. Quântica continuou a pensar e, ao \\nlembrar do rosto da produtora, percebeu um \\nolhar de preocupação vindo dela.  \\n Quântica ainda morava com o seu pai, pois a vida \\nde seu pai após a morte de sua mãe foi vivida \\npara ela, e Quântica, por ser uma mulher de \\npoucos relacionamentos concretos, até porque \\nnão se importava muito, já que a única vez que \\ntinha feito sexo com um homem gerou um \\ntrauma involuntário,  gostava de morar com seu \\npai, um ajudava ao outro e o seu pai conseguia \\nviver uma vida melhor, Quântica olhava para o \\nseu pai e enxergava a necessidade dele em viver, \\nmas, devido a se pri var de sua vida, esqueceu \\ncomo se vive a própria vida, ele queria ser",
      "position": 119084,
      "chapter": 5,
      "page": 100,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.709199999999996,
      "complexity_metrics": {
        "word_count": 250,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 50.0,
        "avg_word_length": 4.364,
        "unique_word_ratio": 0.576,
        "avg_paragraph_length": 250.0,
        "punctuation_density": 0.136,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "quântica",
          "acordo",
          "viver",
          "dívida",
          "produtora",
          "dela",
          "fazemos",
          "oportunidade",
          "percebeu",
          "outro",
          "pois",
          "raciocínio",
          "teve",
          "quanto",
          "encaixava",
          "esse",
          "pensamento",
          "diante",
          "começou"
        ],
        "entities": [
          [
            "raciocínio que",
            "PERSON"
          ],
          [
            "quanto se encaixava",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "fazemos",
            "PERSON"
          ],
          [
            "se não fazemos",
            "PERSON"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "Quântica",
            "ORG"
          ],
          [
            "valor de dívida perante o \\noutro",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "se eu caso e",
            "PERSON"
          ]
        ],
        "readability_score": 73.6908,
        "semantic_density": 0,
        "word_count": 250,
        "unique_words": 144,
        "lexical_diversity": 0.576
      },
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "id": 1,
      "text": "exemplo para a sua filha, assim ele abdicou de \\napresentar uma nova mulher para a sua filha, \\ncom medo de Quântica se afastar dele, e ele, por \\nser pai, não queria contar para a sua filha p ara ela \\nnão ficar com o peso de ter destruído a vida de \\nseu pai. Quântica entendia e compreendia, porém \\nficou tanto tempo sem prestar atenção aos sinais \\nde energia que ela sentia, que não prestou \\natenção na energia do seu pai de amar uma outra \\npessoa.  \\nQuân tica, ao chegar em casa naquela noite, fez \\numa pergunta para o seu pai:  \\nPai, qual é o valor da sua moeda?  \\nSeu pai sem entender nada, fez uma cara de \\ninterrogação.  \\nQuântica explicou o que acontecera com ela e a \\nprodutora, seu pai olhou para a sua filha e \\nrespondeu: o valor da minha moeda é o valor da \\nminha dívida sentimental em ver a sua felicidade!  \\nQuântica olhou para o seu pai, beijou, abraçou, \\nfalou que o ama e dormiu abraçada com ele.",
      "position": 120574,
      "chapter": 5,
      "page": 101,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.13607843137255,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 28.333333333333332,
        "avg_word_length": 4.211764705882353,
        "unique_word_ratio": 0.5882352941176471,
        "avg_paragraph_length": 170.0,
        "punctuation_density": 0.13529411764705881,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "filha",
          "quântica",
          "valor",
          "atenção",
          "energia",
          "moeda",
          "olhou",
          "minha",
          "exemplo",
          "assim",
          "abdicou",
          "apresentar",
          "nova",
          "mulher",
          "medo",
          "afastar",
          "dele",
          "queria",
          "contar",
          "ficar"
        ],
        "entities": [
          [
            "nova",
            "LOC"
          ],
          [
            "medo de Quântica",
            "PERSON"
          ],
          [
            "não queria contar",
            "PERSON"
          ],
          [
            "ara ela \\nnão ficar",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "compreendia",
            "GPE"
          ],
          [
            "sem prestar atenção aos sinais \\nde energia",
            "ORG"
          ],
          [
            "ela sentia",
            "PERSON"
          ],
          [
            "seu pai de amar uma outra \\npessoa",
            "ORG"
          ],
          [
            "casa naquela noite",
            "ORG"
          ]
        ],
        "readability_score": 84.56980392156862,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 100,
        "lexical_diversity": 0.5882352941176471
      },
      "preservation_score": 1.1088695393091642e-05
    },
    {
      "id": 1,
      "text": "Capítulo 2 3 loucuras de um viver  \\nQuântica chegava aos seus 30 anos, ela que \\nnasceu em 1988, já tinha vivido na década de 90 e \\nnos anos 2000, vivendo a transição de uma era \\nindustrial para uma era tecnológica que, devido \\nao ano em que ela nasceu, a vida que ela viveu \\nsomada a necessidade de se trabalhar para ajudar \\nseu pai em manter as contas da casa, comida, \\ndiversão, a fez, involuntariamente, obter um \\ncrescimento sem ter a necessidade de fazer \\nfaculdade ou estudar muito sobre tecnologia, pois \\na forma que ela trabalhava, já supria a \\nnecessidade de entendimento que ela  precisava \\npara o seu trabalho. Os seus amigos que não \\ntiveram a oportunidade ( qualidade, caráter do \\nque é oportuno , vem de oportuno, logo eu penso \\nque a nossa oportunidade parte de nós mesmos ), \\nmas como criamos essas oportunidades? Através \\nde julgarmos qu em vai estar ao nosso lado \\ndurante a vida, pois nós somos frutos do meio em \\nque vivemos, seja ele bom ou ruim. O dono do \\nmorro, por exemplo, criou oportunidades no \\nmeio em que ele vive, ele foi gerando contatos \\nsendo bom para cada pessoa, focando no seu \\npróprio benefício, por atingir a oportunidade no \\nmomento propício. Então, para termos uma vida \\nboa, de acordo com o que queremos para nós \\nmesmos, geramos essas oportunidades \\ninvoluntariamente ou voluntariamente? Nós \\nsomos frutos do meio em que vivemos. Se nó s já",
      "position": 121610,
      "chapter": 2,
      "page": 102,
      "segment_type": "page",
      "themes": {
        "filosofia": 31.25,
        "ciencia": 27.083333333333336,
        "arte": 20.833333333333336,
        "tecnologia": 20.833333333333336
      },
      "difficulty": 33.46975493126121,
      "complexity_metrics": {
        "word_count": 239,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 34.142857142857146,
        "avg_word_length": 4.661087866108787,
        "unique_word_ratio": 0.6610878661087866,
        "avg_paragraph_length": 239.0,
        "punctuation_density": 0.13389121338912133,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "necessidade",
          "oportunidade",
          "oportunidades",
          "meio",
          "seus",
          "anos",
          "nasceu",
          "involuntariamente",
          "pois",
          "oportuno",
          "mesmos",
          "essas",
          "somos",
          "frutos",
          "vivemos",
          "capítulo",
          "loucuras",
          "viver",
          "quântica"
        ],
        "entities": [
          [
            "2 3",
            "DATE"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "aos",
            "ORG"
          ],
          [
            "30",
            "CARDINAL"
          ],
          [
            "ela que \\nnasceu",
            "PERSON"
          ],
          [
            "1988",
            "DATE"
          ],
          [
            "já tinha vivido na década de 90",
            "PERSON"
          ],
          [
            "2000",
            "DATE"
          ],
          [
            "ela nasceu",
            "PERSON"
          ],
          [
            "ela viveu \\nsomada",
            "PERSON"
          ]
        ],
        "readability_score": 81.5302450687388,
        "semantic_density": 0,
        "word_count": 239,
        "unique_words": 158,
        "lexical_diversity": 0.6610878661087866
      },
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "id": 1,
      "text": "nascemos com menos chances de ter uma vida \\ndigna diante de uma sociedade, quais são as \\nchances de crescermos na vida dignamente com \\nas nossas próprias oportunidades? De crescer na \\nvida semelhante a Quântica? Precisaram evoluir \\nos seus estudos junto a evolução tecnológica, \\nporém, as crianças de hoje em dia já nascem com \\num telefone na mão, o costume deles o usarem \\nno dia a dia, a quantidade de informações com \\nmais acessibilidades, que antes nós não tínhamos, \\nfaz os amigos de Quântica terem dificuldades em \\narrumar emprego e se profissionalizar à altura de \\numa qualidade profissional para se ter um \\nemprego.  \\nQuântica como não sabia usar a tecnologia com \\nprofundidade, mas sabia desenrolar mais coisas \\nque a maioria das pessoas de sua idade, se \\ninscreveu em um aplicativo de relacionamento, \\nesse aplicativo disponibilizava as opções de sexo, \\nidade, altura, tinha que falar sobre o que ela \\ngosta de comer e fazer. Ela colocou no perfil dela \\no interesse em mulheres, com idade entre 20 e 50 \\nanos e uma aproximação de 10  km. \\nUm belo dia, Quântica estava em casa após o seu \\ntrabalho, fumando seu baseado, pois era o seu \\nmomento de sentir conforto após um dia \\ncansativo, sua rotina normalmente resumia -se a \\nchegar em casa, jantar, tomar banho e se deitar \\npara dormir, já que no dia seguinte teria que \\ntrabalhar novamente, porém, naquela noite,",
      "position": 123110,
      "chapter": 5,
      "page": 103,
      "segment_type": "page",
      "themes": {
        "filosofia": 39.473684210526315,
        "ciencia": 34.21052631578947,
        "tecnologia": 26.31578947368421
      },
      "difficulty": 35.54141193595342,
      "complexity_metrics": {
        "word_count": 229,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 38.166666666666664,
        "avg_word_length": 4.860262008733624,
        "unique_word_ratio": 0.6462882096069869,
        "avg_paragraph_length": 229.0,
        "punctuation_density": 0.12663755458515283,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "vida",
          "idade",
          "chances",
          "porém",
          "mais",
          "emprego",
          "altura",
          "sabia",
          "aplicativo",
          "casa",
          "após",
          "nascemos",
          "menos",
          "digna",
          "diante",
          "sociedade",
          "quais",
          "crescermos",
          "dignamente"
        ],
        "entities": [
          [
            "nascemos",
            "PERSON"
          ],
          [
            "digna diante de uma sociedade",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "dia já nascem",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "nós não tínhamos",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "de Quântica",
            "PERSON"
          ],
          [
            "profissionalizar à",
            "ORG"
          ]
        ],
        "readability_score": 79.45858806404658,
        "semantic_density": 0,
        "word_count": 229,
        "unique_words": 148,
        "lexical_diversity": 0.6462882096069869
      },
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "id": 1,
      "text": "pegou seu telefone e começou a curtir o perfil de \\nvárias mulheres no seu aplicativo e, ali, ela \\nconheceu uma mulher linda.  \\nQuântica marcou um  encontro com ela na sexta -\\nfeira, pois de segunda a sexta Quântica se \\nobrigava a se empenhar no trabalho, visto que \\ndali vinha todo o dinheiro necessário para ela \\nconseguir viver o que queria viver. Ao chegar no \\nlocal marcado com a moça, Quântica sentou à \\nmesa, pediu um chopp, ficou observando os \\nacontecimentos e tudo que chamava a atenção \\nem seu entorno, desde pessoas, situações, vento, \\nas árvores balançando, um beijo de um filho em \\numa mãe, sorriso involuntário, sorriso forçado e \\ntudo que poderia ser notado, pois Quântica \\nestudava o comportamento  das pessoas para \\nmelhor entender a necessidade das pessoas \\nperante o seu próprio trabalho, ela precisava ser \\ncriativa na publicidade e ser criativa na \\npublicidade é entender o que um contexto \\nprecisa de acordo com o produto do contratante. \\nEssa forma de o bservação veio por meio do \\naprendizado de sua mãe, já que, todos os \\ndomingos, sua mãe, seu pai e ela iam passear em \\nfamília sem destino, até porque a necessidade do \\npasseio é valorizar o viver o mundo real e, através \\ndesse aprendizado, Quântica fazia isso no seu dia \\na dia involuntariamente, de tanto praticar esse \\nestilo de vida.",
      "position": 124599,
      "chapter": 5,
      "page": 104,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.44434389140271,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.25,
        "avg_word_length": 4.8144796380090495,
        "unique_word_ratio": 0.6244343891402715,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.12669683257918551,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "viver",
          "pessoas",
          "sexta",
          "pois",
          "trabalho",
          "tudo",
          "sorriso",
          "entender",
          "necessidade",
          "criativa",
          "publicidade",
          "aprendizado",
          "pegou",
          "telefone",
          "começou",
          "curtir",
          "perfil",
          "várias",
          "mulheres"
        ],
        "entities": [
          [
            "pegou seu",
            "ORG"
          ],
          [
            "perfil de \\nvárias",
            "ORG"
          ],
          [
            "ali",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "linda",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para ela \\nconseguir viver o",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ]
        ],
        "readability_score": 70.93065610859729,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 138,
        "lexical_diversity": 0.6244343891402715
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "Quântica olhou para a sua frente e viu uma \\nmenina linda de olhos verdes, cabelos longos e \\ndourados com uma luz própria emergindo dela. \\nQuântica, ao olhar, só lembrava dos elfos dos \\ncontos, livros e de filmes que ela tinha visto. Essa \\nElfa se aproximou dela, se apresentou e abriu um \\nsorriso simpático, Quântica, por sentir a energia \\ndas pessoas e prometer a ela mesma que seguiria \\na sua intuição, logo no primeiro momento que as \\nduas for am se cumprimentar, a abraçou, olhou e \\nfalou: ao olhar para você eu vi algo que eu nunca \\ntinha visto, senti uma empatia que eu nunca \\nhavia sentido, tive uma vontade de a abraçar, \\nmas não havia feito isso antes, pois o fazer algo \\nsem entendimento de quem es tá recebendo o \\nalgo é incompreensível, o sentir é o meu sentir.  \\nElfa retribuiu tudo que a Quântica fez \\ninvoluntariamente, pois sentia o mesmo que ela, \\nas duas sem entender nada, ambas ficaram \\nassustadas e se apresentaram falando ao mesmo \\ntempo. O que é is so? \\nSilêncio, olhar, sentir, apreciar, admirar, até que \\nQuântica conseguiu falar alguma coisa: preciso \\nentender isso que aconteceu, nunca vivi ou \\nconheci uma história assim, vejo contos de \\nprincesas com príncipes, mas não lembro se foi \\ntão espontâneo e rea l. \\nConcordo com todas as suas palavras, até porque \\neu vivi o mesmo que você, senti a mesma energia \\nque você interpretou, ainda tenho algo a",
      "position": 126031,
      "chapter": 5,
      "page": 105,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.39915966386555,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 34.0,
        "avg_word_length": 4.663865546218488,
        "unique_word_ratio": 0.634453781512605,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.15546218487394958,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "sentir",
          "algo",
          "olhar",
          "você",
          "nunca",
          "mesmo",
          "olhou",
          "dela",
          "contos",
          "tinha",
          "visto",
          "elfa",
          "energia",
          "mesma",
          "duas",
          "senti",
          "havia",
          "isso",
          "pois"
        ],
        "entities": [
          [
            "Quântica olhou",
            "ORG"
          ],
          [
            "linda de olhos verdes",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "só lembrava",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "Essa \\nElfa",
            "PERSON"
          ],
          [
            "Quântica",
            "ORG"
          ],
          [
            "das pessoas",
            "PRODUCT"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "você eu",
            "PERSON"
          ]
        ],
        "readability_score": 81.60084033613445,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 151,
        "lexical_diversity": 0.634453781512605
      },
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "id": 1,
      "text": "acrescentar, eu senti um amor, não carnal, e sim \\num amor de confiança, carinho, proteção, \\nrespeito, compreensão e mu itos outros \\nsentimentos sem explicação, devido à raridade de \\nserem vividos — respondeu Elfa.  \\nQuântica puxou outro assunto e começou a fazer \\nperguntas sobre Elfa: onde mora, sobre os pais, a \\nvida cotidiana e bebendo uma cerveja gelada no \\nboteco em Jacarepag uá, conversando sobre as \\nloucuras vividas com os amigos, tudo muito claro \\ne sem mentiras, sem preocupação em contar, \\npois ambas eram dignas e não tinham vergonha \\nda sua vida, viver o certo ou errado, ganhar ou \\nperder é viver a vida.  \\nNós somos o que somos d evido ao nosso próprio \\nviver, se esse meu viver é o errado, irei me \\ndedicar a aprender o certo, até porque nós, \\nhumanos, somos falhos e não queremos aceitar a \\nnossa própria falha, pois não percebemos que \\nfalhamos até a nossa própria falha voltar para si \\npróprio.  \\n— Qual é a sua história mais louca? — perguntou \\nQuântica.  \\n— Uma das, pois não sei quantas vivi, umas eu \\nnão lembro por estar bêbada; outras, por ter \\nusado outros tipos de drogas, porém uma foi bem \\ninteressante (que desperta interesse, que motiva, \\nque não entedia. Que se revela útil, que traz \\nvantagem material, financeira etc. Algo que é",
      "position": 127525,
      "chapter": 5,
      "page": 106,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.9125,
      "complexity_metrics": {
        "word_count": 216,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 4.708333333333333,
        "unique_word_ratio": 0.7314814814814815,
        "avg_paragraph_length": 216.0,
        "punctuation_density": 0.18055555555555555,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "vida",
          "pois",
          "somos",
          "amor",
          "outros",
          "elfa",
          "quântica",
          "certo",
          "errado",
          "próprio",
          "nossa",
          "própria",
          "falha",
          "acrescentar",
          "senti",
          "carnal",
          "confiança",
          "carinho",
          "proteção"
        ],
        "entities": [
          [
            "acrescentar",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "amor de confiança",
            "ORG"
          ],
          [
            "respeito",
            "GPE"
          ],
          [
            "compreensão e mu itos outros \\n",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "Elfa",
            "PERSON"
          ],
          [
            "Jacarepag",
            "PERSON"
          ],
          [
            "tudo muito claro \\ne",
            "PERSON"
          ],
          [
            "mentiras",
            "PERSON"
          ]
        ],
        "readability_score": 85.0875,
        "semantic_density": 0,
        "word_count": 216,
        "unique_words": 158,
        "lexical_diversity": 0.7314814814814815
      },
      "preservation_score": 2.9698418965845438e-05
    },
    {
      "id": 1,
      "text": "instigante. Algo que vale apena tentar.) — \\nrespondeu Elfa.  \\n— A primeira vez que fui em uma rave — \\ncontinuou —, viu que já começou boa, percebeu \\nlogo que tem drogas? Aí, eu estava lá, com 32 \\nanos, feliz e contente por ter arrumado o \\nemprego da minha vida, comemorando com \\nvárias amigas engraçadas aquela minha \\nconquista, fui tomar bala e poucas vezes em \\nminha vida eu tinha tomado, perguntei a uma \\namiga qual a quantidade a tomar, tomei um \\nterço. No início, foi sensacional, foi a perfeição da \\nfelicidade, pois sentia todas as minhas amigas \\nconectadas comigo, dançando, conversando algo \\nque ninguém entendia, ficávamos sorrindo uma \\npara a outra, pois todos os assuntos, por pior es \\nque fossem, eram engraçados, todas estavam \\nsorrindo muito e a onda da bala é uma onda que \\nvai e volta toda hora, mas foi aí que aconteceu a \\nmerda! Eu, inexperiente, pensei que a onda tinha \\npassado, perguntei a uma amiga quando era para \\ntomar outra parte . Minha amiga pegou o restante \\nda bala e jogou pela minha boca adentro, pois ela \\nnão estava escutando, estava sorrindo e, pelo \\nmeu sorriso, ela pensou que eu queria o restante. \\nAí fodeu a porra toda, a rave era próxima a minha \\ncasa, e eu, linda e bela, res olvi ir embora, até \\nporque percebi que estava vindo uma onda muito \\nlouca, fiquei pensando que ia dar merda, percebia",
      "position": 128906,
      "chapter": 5,
      "page": 107,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.378205128205128,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 4.594017094017094,
        "unique_word_ratio": 0.6752136752136753,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.1794871794871795,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "estava",
          "onda",
          "tomar",
          "bala",
          "amiga",
          "pois",
          "sorrindo",
          "algo",
          "rave",
          "vida",
          "amigas",
          "tinha",
          "perguntei",
          "todas",
          "outra",
          "muito",
          "toda",
          "merda",
          "restante"
        ],
        "entities": [
          [
            "apena tentar.",
            "PERSON"
          ],
          [
            "já começou boa",
            "PERSON"
          ],
          [
            "eu estava lá",
            "PERSON"
          ],
          [
            "32",
            "CARDINAL"
          ],
          [
            "várias amigas",
            "PERSON"
          ],
          [
            "engraçadas",
            "PRODUCT"
          ],
          [
            "aquela minha \\nconquista",
            "PERSON"
          ],
          [
            "fui tomar bala",
            "PERSON"
          ],
          [
            "minhas amigas \\n",
            "PERSON"
          ],
          [
            "conectadas",
            "PRODUCT"
          ]
        ],
        "readability_score": 85.62179487179488,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 158,
        "lexical_diversity": 0.6752136752136753
      },
      "preservation_score": 3.172331116806217e-05
    },
    {
      "id": 1,
      "text": "que não ia lembrar o que poderia acontecer. E eu \\nestava certa!  \\n— Ao caminhar, parei no banheiro para fazer xixi, \\nestava com o telefone e mi nha carteira nas mãos, \\ncoloquei minhas coisas em cima de uma \\n“prateleira” para apoiar as minhas mãos em \\nalgum lugar, para eu não encostar minha bunda \\nnaquele banheiro químico. Sem perceber e \\nfuturamente percebendo, notei que não fui \\nembora. Acordei sentada  em uma árvore com um \\nsegurança do evento me perguntando se eu sabia \\nonde eu estava. Eu respondi corretamente que \\nestava em uma festa.  \\n— Está tudo bem com você? — indagou o \\nsegurança.  \\n— Sim, fiz alguma besteira? — questionei.  \\n— Não fez besteira nenhuma! — respondeu.  \\n— Tem certeza?  — insisti.  \\n— Tenho sim, você parecia um cachorro feliz e \\ncontente abraçando as árvores e rolando na \\ngrama sozinha! Você está muito louca, tem \\nalguma amiga ou amigo que esteja aqui com \\nvocê? — ele perguntou.  \\n— Estão na festa — eu disse e, então, o segurança \\nme levou até as minhas amigas, que perguntaram \\nonde eu estava. Eu logo respondi onde e apontei \\no local. Uma amiga minha veio e concluiu: Você é",
      "position": 130360,
      "chapter": 5,
      "page": 108,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 21.218556701030927,
      "complexity_metrics": {
        "word_count": 194,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 9.7,
        "avg_word_length": 4.561855670103093,
        "unique_word_ratio": 0.6701030927835051,
        "avg_paragraph_length": 194.0,
        "punctuation_density": 0.15979381443298968,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estava",
          "você",
          "minhas",
          "segurança",
          "onde",
          "banheiro",
          "mãos",
          "minha",
          "respondi",
          "festa",
          "está",
          "alguma",
          "besteira",
          "amiga",
          "lembrar",
          "poderia",
          "acontecer",
          "certa",
          "caminhar",
          "parei"
        ],
        "entities": [
          [
            "não ia lembrar o",
            "ORG"
          ],
          [
            "xixi",
            "ORG"
          ],
          [
            "nha carteira",
            "PERSON"
          ],
          [
            "nas mãos",
            "PERSON"
          ],
          [
            "cima de uma \\n“prateleira",
            "PERSON"
          ],
          [
            "para apoiar",
            "PERSON"
          ],
          [
            "minhas mãos",
            "PERSON"
          ],
          [
            "algum lugar",
            "PERSON"
          ],
          [
            "para eu não encostar",
            "PERSON"
          ],
          [
            "se eu sabia \\nonde eu estava",
            "PERSON"
          ]
        ],
        "readability_score": 93.78144329896907,
        "semantic_density": 0,
        "word_count": 194,
        "unique_words": 130,
        "lexical_diversity": 0.6701030927835051
      },
      "preservation_score": 2.883060802203827e-05
    },
    {
      "id": 1,
      "text": "a malucona que fritou na rave, rolando na grama \\nsozinha, nós estávamos comentando de  você sem \\nsaber que era você!  \\n— Após 2 dias, eu fui parar no hospital por ter \\ncontraído sarna — ri. Esse dia foi muito bom e \\nnão lembro de muita coisa, porém, pelo  que me \\ncontaram, achei bonito eu ficar em contato com a \\nnatureza, achei bacana eu ficar al ucinada de uma \\nforma dessa, dentro de todos os males há uma \\nbeleza, mas aprendi a nunca mais tomar uma \\ndose de droga tão alta para mim.  \\nQuântica estava vivendo uma vida dos sonhos, \\ntudo em seu entorno continha muito mais \\nfelicidade que tristeza, todos os d ias de sua vida \\ntinha sorrisos, conversas, trabalho, família, amor \\ne tinha também os problemas, estresse, mas ela \\nnem pensava, pois o viver é saber sobreviver, e a \\nforma que ela estava sobrevivendo era a mais \\nsatisfatória do que ela poderia imaginar.  \\nQuântica, com seus 34 anos, encontrou o seu \\namigo anão, que comentou que era seu \\naniversário naquele dia, logo veio um \\npensamento em sua cabeça: Vai dar merda! Sem \\nhesitar, pergunta: Para onde vamos sair? \\nQuântica via felicidade em tudo e se \\ncomprometeu em  seguir toda energia captada, \\nela foi com tudo para mais uma loucura de se \\njogar para a felicidade, sabia que a comemoração \\ndo aniversário de seu amigo ia ser legal, pois,",
      "position": 131590,
      "chapter": 5,
      "page": 109,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.72744853399875,
      "complexity_metrics": {
        "word_count": 229,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 32.714285714285715,
        "avg_word_length": 4.567685589519651,
        "unique_word_ratio": 0.6768558951965066,
        "avg_paragraph_length": 229.0,
        "punctuation_density": 0.1572052401746725,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "quântica",
          "tudo",
          "felicidade",
          "você",
          "saber",
          "muito",
          "achei",
          "ficar",
          "forma",
          "todos",
          "estava",
          "vida",
          "tinha",
          "pois",
          "amigo",
          "aniversário",
          "malucona",
          "fritou",
          "rave"
        ],
        "entities": [
          [
            "nós estávamos",
            "GPE"
          ],
          [
            "de  você sem \\nsaber",
            "PERSON"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "eu fui",
            "PERSON"
          ],
          [
            "muito bom e",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "achei bonito eu ficar",
            "PERSON"
          ],
          [
            "achei bacana eu ficar",
            "PERSON"
          ],
          [
            "al ucinada de uma \\nforma dessa",
            "ORG"
          ],
          [
            "dentro de todos",
            "ORG"
          ]
        ],
        "readability_score": 82.27255146600125,
        "semantic_density": 0,
        "word_count": 229,
        "unique_words": 155,
        "lexical_diversity": 0.6768558951965066
      },
      "preservation_score": 2.5648634561411964e-05
    },
    {
      "id": 1,
      "text": "sempre que esteve com ele, histórias boas \\naconteceram.  \\nEles foram para uma festa em uma favela, \\nchegando nessa favela, o anão conhecia todo \\nmundo, os bandidos o chamavam  de tripé. Toda \\nhora chamavam tripé para cá, tripé para lá, e \\nQuântica a cada vez que escutava isso, olhava \\npara o seu amigo e sorria muito, seu amigo, por \\nsua vez, sent ia orgulho do seu apelido. O caminho \\npara conquistá -lo foi bem interessante, contou  \\nque o seu apelido surgiu devido a sua semelhança \\na um ator pornô e, por isso, uma mulher muito \\nbonita e gostosa ficou curiosa para saber o \\ntamanho, vieram outras, mais out ras, mais \\noutras, graças a semelhança.  \\nQuântica e anão passaram a festa brincando se \\ndivertindo e resolveram prolongar a noite, \\ntiveram que  pegar um ônibus ali, na favela não \\nentra táxi e nem carro de aplicativo, foram parar \\nem uma roda de samba raiz com pessoas \\ncantando no gogó, os instrumentos no barulho \\nnatural, cerveja gelada, mulatas, uma mais bonita \\nque a outra, que o amigo anão não parava de \\nolhar, resolveram comer alguma coisa na rua e \\navistaram aquele  botequim do ovo cor -de-rosa, \\ntorresmo, carne a ssada e até um sanduíche com \\nalface, pernil, queijo, maionese, cebola e ketchup. \\nQuântica e anão mandaram para dentro uma \\nporção de torresmo junto ao ovo rosa servido no",
      "position": 133015,
      "chapter": 5,
      "page": 110,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.079613095238095,
      "complexity_metrics": {
        "word_count": 224,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.333333333333336,
        "avg_word_length": 4.709821428571429,
        "unique_word_ratio": 0.6651785714285714,
        "avg_paragraph_length": 224.0,
        "punctuation_density": 0.16517857142857142,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "anão",
          "favela",
          "tripé",
          "quântica",
          "amigo",
          "mais",
          "festa",
          "chamavam",
          "isso",
          "muito",
          "apelido",
          "semelhança",
          "bonita",
          "outras",
          "resolveram",
          "rosa",
          "torresmo",
          "sempre",
          "esteve",
          "histórias"
        ],
        "entities": [
          [
            "sempre que",
            "ORG"
          ],
          [
            "nessa favela",
            "PERSON"
          ],
          [
            "tripé para lá",
            "PERSON"
          ],
          [
            "para o",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "sua vez",
            "PERSON"
          ],
          [
            "ia orgulho",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ]
        ],
        "readability_score": 79.9203869047619,
        "semantic_density": 0,
        "word_count": 224,
        "unique_words": 149,
        "lexical_diversity": 0.6651785714285714
      },
      "preservation_score": 2.699856269622312e-05
    },
    {
      "id": 1,
      "text": "prato de papelão e, para finalizar, um sanduba  do \\ndia anterior.  \\nQuântica e anão, pensa ndo que ainda eram \\njovens, sem perceber o mal que fizeram aos seus \\ncorpos, sentiram algo estranho acontecer, \\nQuântica, por ter tido uma experiência \\nsemelhante, sabia que vinha merda, literalmente \\nia vir merda.  Kkkkkkk - Quântica e anão, a essa \\naltura do ca mpeonato, encontravam -se em um \\ntotal desespero, tiveram que usar o banheiro do \\npagode, ambos desesperados, entraram no \\nbanheiro rapidamente sem falar muita coisa, se \\nlargaram, sujaram toda a louça do vaso, a merda \\nfoi antigravitacional, pois todo o vaso, i nclusive a \\ntampa do vaso pela parte debaixo. O desespero \\nficou ainda maior quando Quântica percebeu que \\nali não tinha papel higiênico. Rindo sozinha e \\ndesesperada ao mesmo tempo, pensando que, se \\nela contasse aquilo que estava acontecendo com \\nela, todos ia m sorrir, pegou as suas meias de cano \\nbaixo  para se limpar, passou uma vez e a meia \\ndeslizou até a altura das costas, dobrou e passou \\nnovamente, sujando a sua meia de norte a sul, \\npegou a outra meia e passou com mais \\npreocupação, pois só teria mais uma pa ssada \\napós aquela e de nada adiantou, pois deslizou até \\nquase a sua nuca, dobrou no meio novamente \\nolhou para a sua meia e falou: me salva, por \\nfavor, e seja resistente em absorver uma maior",
      "position": 134444,
      "chapter": 5,
      "page": 111,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.41842105263158,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 45.6,
        "avg_word_length": 4.728070175438597,
        "unique_word_ratio": 0.7017543859649122,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.16228070175438597,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "meia",
          "merda",
          "vaso",
          "pois",
          "passou",
          "anão",
          "ainda",
          "altura",
          "desespero",
          "banheiro",
          "maior",
          "pegou",
          "deslizou",
          "dobrou",
          "novamente",
          "mais",
          "prato",
          "papelão",
          "finalizar"
        ],
        "entities": [
          [
            "prato de papelão e",
            "ORG"
          ],
          [
            "para finalizar",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "pensa ndo",
            "PERSON"
          ],
          [
            "ainda eram",
            "PERSON"
          ],
          [
            "sem perceber o mal que",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "literalmente \\nia vir merda.  ",
            "PERSON"
          ],
          [
            "Kkkkkkk - Quântica",
            "ORG"
          ],
          [
            "ambos desesperados",
            "PERSON"
          ]
        ],
        "readability_score": 75.78157894736842,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 160,
        "lexical_diversity": 0.7017543859649122
      },
      "preservation_score": 2.6323598628817546e-05
    },
    {
      "id": 1,
      "text": "quantidade. Quântica saiu do banheiro não muito \\nfeliz, pois senti a que ainda tinha resíduo.  \\nMesmo com toda essa situação, Quântica não \\nestava nem aí para o incômodo, pois, naquela \\naltura do campeonato, nem lembrava mais do \\nincômodo, Quântica e seu amigo anão estavam \\nsem freio, dançando, bebendo, fazendo amizades \\ne sorri ndo com todos próximos aos dois. Seu \\namigo anão, do nada, teve uma ideia genial: \\ntomar um drinque flamejante para animar um \\npouco mais aquela noite. Por que ele fez isso? \\nIsso não foi legal, isso foi a decadência do \\nsentimento adulto de Quântica e anão, el es \\nresolveram sair do pagode e caminhar enquanto \\nconversavam, quando olharam para o lado e \\nviram um frango gigante, a Quântica pediu para o \\nseu amigo anão tirar foto dela com o frango, \\nenquanto a Quântica ficava se ajeitando para tirar \\nfoto se pendurando n o rabo do frango, o seu \\namigo, muito bêbado, não conseguia se ajeitar \\npara bater uma foto decente, quando, do nada, \\nQuântica arrebentou o rabo do frango e saiu \\nrolando, ela e o rabo do frango. Anão e Quântica \\ndesesperados por terem feito merda, largaram o \\nrabo do frango e saíram correndo iguais a dois \\nadolescentes que acabavam de se divertir a noite \\ntoda. O final de uma noite épica foi tirar uma foto \\ne destruir um patrimônio público \\ninvoluntariamente.",
      "position": 135898,
      "chapter": 5,
      "page": 112,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.431696428571428,
      "complexity_metrics": {
        "word_count": 224,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.0,
        "avg_word_length": 4.772321428571429,
        "unique_word_ratio": 0.6026785714285714,
        "avg_paragraph_length": 224.0,
        "punctuation_density": 0.14732142857142858,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "frango",
          "anão",
          "amigo",
          "foto",
          "rabo",
          "noite",
          "isso",
          "tirar",
          "saiu",
          "muito",
          "pois",
          "toda",
          "incômodo",
          "mais",
          "dois",
          "nada",
          "enquanto",
          "quando",
          "quantidade"
        ],
        "entities": [
          [
            "Quântica",
            "NORP"
          ],
          [
            "não muito \\nfeliz",
            "PERSON"
          ],
          [
            "Mesmo",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "estava nem",
            "PERSON"
          ],
          [
            "naquela \\naltura",
            "ORG"
          ],
          [
            "nem lembrava mais",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "sem freio",
            "PERSON"
          ],
          [
            "todos",
            "NORP"
          ]
        ],
        "readability_score": 84.56830357142857,
        "semantic_density": 0,
        "word_count": 224,
        "unique_words": 135,
        "lexical_diversity": 0.6026785714285714
      },
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "id": 1,
      "text": "Capítulo 2 4 certo ou errado  \\nQuântica e a produtora conve rsavam na sala de \\nsua amiga, Quântica, sempre amorosa e muito \\nobservadora, até para não ser pisada por ser \\n“boazinha”, limitava as situações de sua vida \\nantes de acontecer o pior, pois ela já tinha vivido \\ntantas coisas que, mesmo antes de acontecer, ela \\ncalculava as suas ações diante das falhas de quem \\nela amava.  \\nEstavam as duas na sala quando entrou um dos \\nirmãos da produtora pela porta, gritando para \\ntodos ouvirem: Sua filha da puta, irei te matar, as \\ncoisas que você fez com a nossa família para ter \\numa v ida melhor só para você destruíram nossos \\npais e a todos próximos, você tem essa aparência \\nde boazinha, mas não vale nem o pau que chupa!  \\nQuântica permaneceu assustada após o \\nsegurança colocar “aquele homem” para fora da \\nsala, por não entender o que estava  acontecendo \\ne por sua amiga ser sua amiga há mais de dez \\nanos, ela nunca tinha ouvido falar da família da \\nprodutora, a produtora nunca falou sobre, \\nQuântica ficou intrigada com aquela situação, \\npois tinha sentido uma energia ruim vindo da sua \\nprodutora, n unca antes sentida, só foi sentir \\nquando ela sentiu raiva daquele rapaz, a cara da \\nprodutora mudou, aquele seu comportamento \\nsério e sereno ficou agressivo e ríspido. Quântica, \\nsendo amiga e próxima, sentiu -se no direito de",
      "position": 137494,
      "chapter": 2,
      "page": 114,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.407391304347826,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 57.5,
        "avg_word_length": 4.691304347826087,
        "unique_word_ratio": 0.6652173913043479,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.11739130434782609,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "produtora",
          "quântica",
          "amiga",
          "sala",
          "antes",
          "tinha",
          "você",
          "boazinha",
          "acontecer",
          "pois",
          "coisas",
          "quando",
          "todos",
          "família",
          "aquele",
          "nunca",
          "ficou",
          "sentiu",
          "capítulo",
          "certo"
        ],
        "entities": [
          [
            "2 4",
            "CARDINAL"
          ],
          [
            "sala de \\nsua amiga",
            "ORG"
          ],
          [
            "Quântica",
            "GPE"
          ],
          [
            "muito \\nobservadora",
            "PERSON"
          ],
          [
            "até para não ser pisada por ser \\n",
            "ORG"
          ],
          [
            "situações de sua",
            "ORG"
          ],
          [
            "ela já tinha vivido",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "ela \\ncalculava",
            "PERSON"
          ],
          [
            "suas ações diante",
            "PERSON"
          ]
        ],
        "readability_score": 69.84260869565217,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 153,
        "lexical_diversity": 0.6652173913043479
      },
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "id": 1,
      "text": "perguntar quem era aquele homem que falava \\ndaquela forma, a produtora, por sua vez, estava \\nabalada, tensa e trêmula, bebendo um copo \\nd’água que já se encontrava em cima da mesa, e \\napenas disse a Quântica para esquecer esse \\nassunto: Eu não quero que algumas coisas do \\nmeu passado voltem, c oisas que aconteceram \\nque não importam mais, tudo o que tinha que \\nser, foi do jeito que tinha que ser e tudo que eu \\nprecisava fazer, eu fiz para um bem maior.  \\nQuântica continuou sem entender nada, começou \\na se questionar sobre a dignidade de sua amiga, \\naté que ponto ela é minha amiga ou é minha \\namiga só por interesse , mas ela não tinha como \\nacreditar que uma pessoa daquela tivesse algo \\ntão ruim, ela não tinha como acreditar. O que \\naquela produtora visionária, inteligente, amiga, \\natenciosa poderia ter de rui m? Eu poderia \\nesquecer esse assunto, mas o que eu senti de \\nenergia vindo do corpo dela, eu não posso \\nignorar, por mais que eu a conheça há mais de 10 \\nanos, que tenha me ajudado na minha carreira, \\naté que ponto eu tenho que ser grata pela minha \\nprópria grat idão? Todos nós erramos e \\nacertamos, qual deve ter sido o tamanho desse \\nerro, se é que teve algum erro?  \\nQuântica, ao sair da sala de sua amiga, não \\nconseguia parar de pensar no ocorrido, ela só \\npensava que a sua amiga tinha seus 50 anos e \\nsempre estava fel iz, a produtora era estável e",
      "position": 138951,
      "chapter": 5,
      "page": 115,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.30996015936255,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.833333333333336,
        "avg_word_length": 4.366533864541832,
        "unique_word_ratio": 0.6294820717131474,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.13545816733067728,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amiga",
          "tinha",
          "minha",
          "produtora",
          "quântica",
          "mais",
          "daquela",
          "estava",
          "esquecer",
          "esse",
          "assunto",
          "tudo",
          "ponto",
          "como",
          "acreditar",
          "poderia",
          "anos",
          "erro",
          "perguntar",
          "quem"
        ],
        "entities": [
          [
            "perguntar quem era aquele homem que",
            "PERSON"
          ],
          [
            "daquela forma",
            "PERSON"
          ],
          [
            "por sua vez",
            "ORG"
          ],
          [
            "estava \\nabalada",
            "PERSON"
          ],
          [
            "cima da mesa",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "meu passado voltem",
            "ORG"
          ],
          [
            "jeito que",
            "PERSON"
          ],
          [
            "eu fiz",
            "PERSON"
          ]
        ],
        "readability_score": 77.77337317397078,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 158,
        "lexical_diversity": 0.6294820717131474
      },
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "id": 1,
      "text": "fazia muitos trabalhos, sempre dando muito \\nlucro, sustentava um orfanato para crianças \\nespeciais com escola dentro do próprio local, \\nenfermaria, comida, e eram mais de 50 crianças, \\ntudo isso bancado pela empresa da produtora. \\nQuântica continuou andando, olhou para uma das \\nsalas do escritório e lembrou que o diretor de \\nfotografia era amigo de infância da produtora, \\nentrou na sala e perguntou se poderia conversar \\ncom ele, ela entrou, sentou -se falou sobre o \\nocorrido na sala da produ tora e perguntou se \\nsabia quem era aquele homem e o motivo.  \\n—  Quântica, às vezes, você é muito esperta para \\nentender sobre sentimento e, às vezes, você erra \\npor sentir muito o sentimento, deixando seu \\njulgamento de ver o mal nas pessoas falho, pois \\nvocê ajuda, conversa, compreende, limita as \\npessoas, afasta, mas te m momentos que o seu \\nsentimento fala mais alto que a verdade. Nem \\ntodos a nossa volta são iguais ao seu irmão ou de \\nacordo com um pai uma mãe. Temos pessoas que \\nmatam, e elas têm irmãos que às vezes são as \\nmelhores pessoas do mundo. Temos mães e pais \\nque s ão ladrões e, nem por isso, o filho é ladrão. \\nA nossa produtora, quando era mais nova, \\napanhava muito dos pais dela, os irmãos dela \\neram muito machistas devido ao seu pai ser \\nmilitar, e a mãe da produtora tinha medo do pai, \\nporque ele batia nela com frequê ncia. Em um \\ndeterminado dia, o pai dela bateu tanto em sua",
      "position": 140445,
      "chapter": 5,
      "page": 116,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.865725806451614,
      "complexity_metrics": {
        "word_count": 248,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 31.0,
        "avg_word_length": 4.55241935483871,
        "unique_word_ratio": 0.6854838709677419,
        "avg_paragraph_length": 248.0,
        "punctuation_density": 0.14919354838709678,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "muito",
          "produtora",
          "pessoas",
          "mais",
          "vezes",
          "você",
          "sentimento",
          "dela",
          "crianças",
          "eram",
          "isso",
          "quântica",
          "entrou",
          "sala",
          "perguntou",
          "nossa",
          "temos",
          "irmãos",
          "pais",
          "fazia"
        ],
        "entities": [
          [
            "fazia muitos trabalhos",
            "ORG"
          ],
          [
            "dando muito \\nlucro",
            "PERSON"
          ],
          [
            "50",
            "CARDINAL"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "olhou",
            "GPE"
          ],
          [
            "entrou na",
            "PERSON"
          ],
          [
            "ela entrou",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "muito esperta",
            "PERSON"
          ],
          [
            "sentimento",
            "GPE"
          ]
        ],
        "readability_score": 83.13427419354838,
        "semantic_density": 0,
        "word_count": 248,
        "unique_words": 170,
        "lexical_diversity": 0.6854838709677419
      },
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "id": 1,
      "text": "mãe, que sua mãe fugiu de casa com a produtora \\npara a casa de uma amiga, lá elas ficaram 3 \\nmeses, depois se mudaram para outra casa.  \\n— Passaram alguns anos, o pai da produtora tinha \\numa condição de  vida muito boa, pois ele tinha \\numa carreira militar, sua mãe já tinha falecido, o \\npai estava com câncer em estágio muito \\navançado, a produtora viu uma oportunidade de \\npegar todo o dinheiro do pai dela e não pensou \\nduas vezes, era ou vai, ou racha. A produ tora \\npegou todo o dinheiro de sua família e construiu a \\nprodutora.  \\nQuântica sempre ficava pensando o motivo de \\ntantos erros ocorrerem, não compreendia a \\nnecessidade de o  humano querer tanto um viver \\nque ele nem sabe viver, pois ninguém sabe o que \\no faz feliz  e o que faz triste, se você não fizer \\nalguma ação, alguma situação, algo que crie uma \\nmemória, mas, no entanto, é preciso que lembrar \\nde se colocar no lugar do outro, pois se eu fiz com \\no outro, eu aceito que façam comigo.  \\nElfa e Quântica foram passar um final de semana \\nna casa de um amigo médico de Elfa. Quântica já \\nsabia de algumas informações e tinha alguma \\nintimidade, pois já haviam jantado, almoçado, \\nsaído juntos e outras coisas de amigos que vivem \\nbem em um cotidiano, Quântica sabia da criação \\ndele e m uma família tradicional de médicos, \\nquase todos de sua família seguiram a carreira;",
      "position": 141969,
      "chapter": 5,
      "page": 117,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.32520661157025,
      "complexity_metrics": {
        "word_count": 242,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 40.333333333333336,
        "avg_word_length": 4.417355371900826,
        "unique_word_ratio": 0.6033057851239669,
        "avg_paragraph_length": 242.0,
        "punctuation_density": 0.128099173553719,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "casa",
          "produtora",
          "tinha",
          "pois",
          "quântica",
          "família",
          "alguma",
          "muito",
          "carreira",
          "todo",
          "dinheiro",
          "viver",
          "sabe",
          "outro",
          "elfa",
          "sabia",
          "fugiu",
          "amiga",
          "elas",
          "ficaram"
        ],
        "entities": [
          [
            "mãe",
            "ORG"
          ],
          [
            "fugiu de casa",
            "ORG"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "se mudaram para",
            "PERSON"
          ],
          [
            "vida muito boa",
            "PERSON"
          ],
          [
            "sua",
            "ORG"
          ],
          [
            "muito \\navançado",
            "PERSON"
          ],
          [
            "dinheiro de sua",
            "ORG"
          ],
          [
            "pensando o",
            "ORG"
          ],
          [
            "motivo de \\ntantos",
            "PERSON"
          ]
        ],
        "readability_score": 78.50812672176309,
        "semantic_density": 0,
        "word_count": 242,
        "unique_words": 146,
        "lexical_diversity": 0.6033057851239669
      },
      "preservation_score": 2.1598850156978503e-05
    },
    {
      "id": 1,
      "text": "uns cirurgiões, outros anestesistas, tudo no \\ncaminho para o lado de manusear instrumentos, \\npois a família amava arte e veio de uma cadeia de \\nDNA artístico; involuntariame nte, a família tinha \\numa predisposição a ser artista e manusear as \\nmãos com habilidade, tinha uma certa facilidade \\nem deixar as mãos o mais próximo de estar em \\nestabilidade, mas ela nunca tinha ido à casa da \\nfamília do médico, não sabia como era a criação \\ndele e das pessoas em seu entorno, assim que ela \\nchegou na casa de campo da família do médico, \\npercebeu que os trabalhadores daquela família \\neram todos negros, bem felizes, porém negros.  \\nAquilo ali instigou a Quântica e começou a \\nlembrar de situações, de m omentos com o \\nmédico, percebera, assim, alguns sintomas de \\nestereótipos preconceituosos (algum julgamento \\nfeito sem perceber, como por exemplo um pobre  \\nse sentir menor que um rico apenas por ser \\npobre. Homem ter direito de trair ou fazer sexo e \\numa mulher  não, “pensamento machista”.) em \\nalgumas ocasiões. Essas ocasiões eram sempre \\ncom os amigos negros, inclusive com a Quântica \\nno início do relacionamento de amizade que \\ncomeçava a se construir. No início, ele a tratava \\nde forma a não considerá -la inteligent e, capaz, \\ntudo que a Quântica fazia, ele desacreditava, a \\nprofissão e a falta de estudo da Quântica o deixou \\ncom uma cara de perplexo.",
      "position": 143430,
      "chapter": 5,
      "page": 118,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 35.46035242290749,
      "complexity_metrics": {
        "word_count": 227,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.833333333333336,
        "avg_word_length": 4.86784140969163,
        "unique_word_ratio": 0.6519823788546255,
        "avg_paragraph_length": 227.0,
        "punctuation_density": 0.13215859030837004,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "família",
          "quântica",
          "tinha",
          "médico",
          "negros",
          "tudo",
          "manusear",
          "mãos",
          "casa",
          "como",
          "assim",
          "eram",
          "pobre",
          "ocasiões",
          "início",
          "cirurgiões",
          "outros",
          "anestesistas",
          "caminho",
          "lado"
        ],
        "entities": [
          [
            "uns cirurgiões",
            "ORG"
          ],
          [
            "lado de manusear",
            "ORG"
          ],
          [
            "amava arte",
            "PERSON"
          ],
          [
            "veio de uma",
            "PERSON"
          ],
          [
            "artístico",
            "ORG"
          ],
          [
            "involuntariame nte",
            "PERSON"
          ],
          [
            "mãos o",
            "PERSON"
          ],
          [
            "mais próximo de estar",
            "PERSON"
          ],
          [
            "mas ela",
            "PERSON"
          ],
          [
            "ido",
            "ORG"
          ]
        ],
        "readability_score": 79.62298091042584,
        "semantic_density": 0,
        "word_count": 227,
        "unique_words": 148,
        "lexical_diversity": 0.6519823788546255
      },
      "preservation_score": 2.3623742359195235e-05
    },
    {
      "id": 1,
      "text": "No início, tudo, para o médico, resultava de \\npensar que os negros eram inferiores, devido a \\nnão ter convivência com muito s negros no meio \\nsocial em que ele foi criado, pois o meio social era \\nde ricos, pessoas influentes e, nesse meio, a \\nquantidade de negros é escassa. Ele não \\nconversava e nem brincava com pessoas negras, \\nos funcionários da casa, os negros, sempre \\nestavam ser vindo a ele, por mais que ele tivesse \\num afeto de amor imensurável, o respeito do \\nfuncionário era de funcionário da família, assim \\nele foi criando seus pensamentos, a cor de um e a \\ncor do outro era de “inferior”. Após conhecer a \\nQuântica por um tempo e est ar muito presente \\nna vida dela e de  Elfa —  ele foi criado junto com \\nElfa, ele nunca teve um amigo negro tão próximo \\nem viver no mesmo nível “social” e estrutural — \\nfoi, involuntariamente, desfazendo os seus \\npreconceitos, pensamentos de nunca ter vivido, e \\nsó lido.  \\nEsse final de semana é uma coisa rara na vida \\ndesse médico, ele nunca parava de trabalhar, sua \\nprofissão cobrava muito tempo dele. Ingressou na \\nfaculdade aos 19 anos, foram 13 anos estudando \\nsem parar, lidando com vidas e vivendo só para \\nser méd ico, aos 32 anos, ele começou a \\nestruturar sua vida, pois ali ele percebera que \\nestava na hora de ter alguém com que pudesse \\ncontar nas poucas horas que tinha para viver e, \\nquando dispunha dessas poucas horas, ele estava",
      "position": 144910,
      "chapter": 5,
      "page": 119,
      "segment_type": "page",
      "themes": {},
      "difficulty": 42.36153846153846,
      "complexity_metrics": {
        "word_count": 247,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 49.4,
        "avg_word_length": 4.538461538461538,
        "unique_word_ratio": 0.6275303643724697,
        "avg_paragraph_length": 247.0,
        "punctuation_density": 0.13360323886639677,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "negros",
          "muito",
          "meio",
          "social",
          "vida",
          "nunca",
          "anos",
          "médico",
          "criado",
          "pois",
          "pessoas",
          "funcionário",
          "seus",
          "pensamentos",
          "tempo",
          "elfa",
          "viver",
          "estava",
          "poucas",
          "horas"
        ],
        "entities": [
          [
            "para o médico",
            "PERSON"
          ],
          [
            "resultava de \\npensar",
            "PERSON"
          ],
          [
            "muito s negros",
            "PERSON"
          ],
          [
            "nesse meio",
            "PERSON"
          ],
          [
            "Ele",
            "PERSON"
          ],
          [
            "nem brincava",
            "PERSON"
          ],
          [
            "cor",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "muito presente",
            "PERSON"
          ]
        ],
        "readability_score": 73.93846153846154,
        "semantic_density": 0,
        "word_count": 247,
        "unique_words": 155,
        "lexical_diversity": 0.6275303643724697
      },
      "preservation_score": 2.7263727151275312e-05
    },
    {
      "id": 1,
      "text": "cansado e sem motivação para sair d e casa, \\ntransformando -o em escravo do sistema, com \\ndesejos e ambições proporcionais a um evoluir \\nsua própria vida, de acordo com sua necessidade \\nde um viver o presente em coerência com o que \\nviveu no seu passado, nunca deixando de planejar \\no seu futuro. El e vive o melhor no presente, pois \\no próprio nome, presente, já fala tudo sobre \\ncomo devemos viver, devemos viver o presente \\ncomo se nós tivéssemos ganhado um presente de \\nalguém que amamos muito, durante o dia todo, \\nisso acontece com várias pessoas e situaç ões \\ndiferentes, sempre com o pensamento de que o \\npresente é um presente, não importando o que \\nestá acontecendo, até porque, se está \\nacontecendo, em algum momento eu dei \\nliberdade em conhecer aquela pessoa, em ter \\nfeito algo que me faz estar vivendo o que e u \\nestou vivendo, e a morte, doença, caso do acaso \\nsão normais acontecerem no fluxo da vida.  \\nO médico sempre ficava feliz quando desfrutava \\nde um tempo para estar com seus amigos, ele \\nachava que aquele momento era a maior \\nconquista dele, pois toda a sua ded icação, todo o \\nseu esforço valia apena por estar com pessoas \\nque ele ama, e esses momentos de muita fartura, \\nmuito conforto eram necessários devido ao \\nexcesso de trabalho e cobrança perante a um \\npadrão social que ele “precisava manter” em \\nvirtude do meio e m que ele vive, pois sua",
      "position": 146426,
      "chapter": 6,
      "page": 120,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.3698347107438,
      "complexity_metrics": {
        "word_count": 242,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 80.66666666666667,
        "avg_word_length": 4.566115702479339,
        "unique_word_ratio": 0.640495867768595,
        "avg_paragraph_length": 242.0,
        "punctuation_density": 0.1115702479338843,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "presente",
          "viver",
          "pois",
          "vida",
          "vive",
          "como",
          "devemos",
          "muito",
          "todo",
          "pessoas",
          "sempre",
          "está",
          "acontecendo",
          "momento",
          "vivendo",
          "cansado",
          "motivação",
          "sair",
          "casa",
          "transformando"
        ],
        "entities": [
          [
            "motivação",
            "ORG"
          ],
          [
            "evoluir \\nsua própria",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "deixando de planejar \\no",
            "PERSON"
          ],
          [
            "já fala",
            "PERSON"
          ],
          [
            "nós tivéssemos ganhado",
            "ORG"
          ],
          [
            "amamos muito",
            "PERSON"
          ],
          [
            "durante",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "pensamento de que",
            "ORG"
          ]
        ],
        "readability_score": 58.29683195592286,
        "semantic_density": 0,
        "word_count": 242,
        "unique_words": 155,
        "lexical_diversity": 0.640495867768595
      },
      "preservation_score": 2.0972097808673316e-05
    },
    {
      "id": 1,
      "text": "aparência, sua forma de falar, sua vestimenta, \\ntudo é julgado por olharem para ele e \\ninterpretarem que um médico precisava se \\ncomportar de tal forma, se vestir de tal forma, \\nviver e ter um estilo de vida semelhante ao meio \\nem que v ocê vive, até porque ele nem sabia como \\noutro meio social vivia.  \\nUma das empregadas do médico tinha um filho, \\nessa empregada doméstica tinha uma casa na \\nfavela e, por algumas vezes, o filho de sua \\nempregada ia para o trabalho com a mãe, pois a \\nmãe não tinh a condições de deixá -lo com alguém \\nquando não tinha aula, e os colégios públicos \\ntoda hora ficam sem água, a estrutura de \\ntrabalho para se dar um bom estudo é escassa, os \\nprofessores fazem uma faculdade de matemática, \\nfísica, letras, geografia, história, a rte, filosofia e \\nnão sabem ensinar, pois só aprenderam a \\nmatéria, e não técnicas para se dar um estudo \\nmelhor, os alunos, muitas vezes, não têm comida \\nem casa, não têm uma estrutura familiar de ter \\numa calma para estudar, não têm um \\ndirecionamento de respe ito, carinho, afeto, amor, \\nconfiança, companheirismo, necessidade, família \\ne, juntando todos esses desentendimentos da \\nnecessidade para se ter um bom estudo, os \\ncolégios públicos, constantemente, não \\nconseguem realizar todas as aulas na semana.  \\nO médico, a pós conhecer Quântica e ver o quanto \\nele fazia “mal” sem perceber, se aproximou de",
      "position": 147919,
      "chapter": 6,
      "page": 121,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 40.43047210300429,
      "complexity_metrics": {
        "word_count": 233,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 77.66666666666667,
        "avg_word_length": 4.76824034334764,
        "unique_word_ratio": 0.6437768240343348,
        "avg_paragraph_length": 233.0,
        "punctuation_density": 0.1759656652360515,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "médico",
          "tinha",
          "estudo",
          "meio",
          "filho",
          "empregada",
          "casa",
          "vezes",
          "trabalho",
          "pois",
          "colégios",
          "públicos",
          "estrutura",
          "necessidade",
          "aparência",
          "falar",
          "vestimenta",
          "tudo",
          "julgado"
        ],
        "entities": [
          [
            "aparência",
            "PERSON"
          ],
          [
            "sua forma de",
            "PERSON"
          ],
          [
            "julgado",
            "GPE"
          ],
          [
            "olharem",
            "ORG"
          ],
          [
            "para ele e \\ninterpretarem",
            "PERSON"
          ],
          [
            "vestir de tal forma",
            "PERSON"
          ],
          [
            "outro meio",
            "PERSON"
          ],
          [
            "Uma das empregadas",
            "PERSON"
          ],
          [
            "essa empregada",
            "ORG"
          ],
          [
            "filho de sua \\nempregada",
            "ORG"
          ]
        ],
        "readability_score": 59.73619456366237,
        "semantic_density": 0,
        "word_count": 233,
        "unique_words": 150,
        "lexical_diversity": 0.6437768240343348
      },
      "preservation_score": 3.07590767860542e-05
    },
    {
      "id": 1,
      "text": "sua empregada e aprendeu a valorizar, conversar, \\ncompreender, tratar, ser direcionado, direcionar \\ne viver melhor com mais felicidade e amor. Um \\ndia, a sua empregada conversa ndo com o médico \\no fez perceber o quanto o filho de sua empregada \\nse sentia inferior quando ia para a sua casa, o \\nfilho de sua empregada, ao falar com o médico, o \\nchamava de doutor dentro de sua própria casa, \\nbaixava a cabeça e falava de uma forma submissa  \\ne muitos outros sintomas de se sentir inferior \\ndevido ao dinheiro, a casa, ao fato de ser médico, \\nde ter estudo e uma aparência de “respeito”, \\ntudo isso de uma forma involuntária de ambas as \\npartes, pois um foi criado através de uma forma \\nde ver a vida; e  outro, por uma outra forma de \\nver a vida, o médico não gostava de ser chamado \\nde doutor, senhor, chefe, patrão ou qualquer \\noutra referência de escala social, pois ele achava \\nque quem o chamava assim fora de seu local de \\ntrabalho já se colocava como inferi or na sua \\nprópria vida, ninguém é melhor que ninguém fora \\nde um local de trabalho, todos nós somos civis e \\ntemos o mesmo direito de viver, e ele, sendo civil, \\ntem um nome, esse nome é a forma que ele gosta \\nde ser chamado para ter uma relação de um \\nconquist ar a confiança e o direito de um viver, um \\npara com o outro, de se respeitar.  \\nQuântica, Elfa, o médico, a esposa, a empregada e \\nseu filho conversavam no sítio, sorrindo, \\nbrincando, vivendo e todos colaborando em",
      "position": 149410,
      "chapter": 6,
      "page": 122,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 34.618631178707226,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 87.66666666666667,
        "avg_word_length": 4.3688212927756656,
        "unique_word_ratio": 0.532319391634981,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.1482889733840304,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "empregada",
          "médico",
          "forma",
          "viver",
          "filho",
          "casa",
          "vida",
          "melhor",
          "inferior",
          "chamava",
          "doutor",
          "própria",
          "pois",
          "outro",
          "outra",
          "chamado",
          "fora",
          "local",
          "trabalho",
          "ninguém"
        ],
        "entities": [
          [
            "sua empregada",
            "FAC"
          ],
          [
            "tratar",
            "ORG"
          ],
          [
            "fez perceber o quanto",
            "ORG"
          ],
          [
            "filho de sua",
            "ORG"
          ],
          [
            "quando ia",
            "PERSON"
          ],
          [
            "filho de sua empregada",
            "ORG"
          ],
          [
            "dentro de sua própria",
            "ORG"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "fato de ser médico",
            "ORG"
          ],
          [
            "uma aparência de “respeito",
            "PERSON"
          ]
        ],
        "readability_score": 54.85602027883397,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 140,
        "lexical_diversity": 0.532319391634981
      },
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "id": 1,
      "text": "ajudar na comida, arrumação, em executar tod as \\nas necessidades naquele sítio, até porque o fazer \\numa comida é uma arte, o plantar é uma arte, o \\nconversar é uma arte, tudo que contém \\nsentimentos é arte.  \\nQual é o valor de uma música que faz sucesso?  \\nQual é o valor de um livro que faz sucesso?  \\nQual é o  valor de um artista que faz sucesso?  \\nQual é o valor monetário do sentimento perante \\na arte?  \\nO excesso de conforto é deixar de viver o melhor \\nde se viver, energia é gerada através do \\nmovimento, se nós não nos movermos, do que \\nadianta vivermos?  \\nA vida é igu al a um jogo de xadrez. Cada \\nmovimento pensado, terá consequência junto ao \\nmovimento do passado, ligado ao movimento do \\npresente, afetando o movimento do seu futuro.  \\nQuântica e Elfa estavam no sítio bebendo, \\nfumando maconha e se divertindo muito, \\nQuântica notou uma caixa de papelão, viu um \\nbarranco de grama dentro do sítio e teve a \\ngrande ideia de descer deslizando dentro da \\ncaixa, Elfa tinha muito mais medo que Quântica e \\nsó falava para Quântica tomar cuidado, mas ela, \\naudaciosa e muito feliz em estar viva , apenas \\npensava em descer aquele barranco e ser feliz",
      "position": 150970,
      "chapter": 6,
      "page": 123,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 27.68695652173913,
      "complexity_metrics": {
        "word_count": 207,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.0,
        "avg_word_length": 4.4396135265700485,
        "unique_word_ratio": 0.5942028985507246,
        "avg_paragraph_length": 207.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "arte",
          "movimento",
          "qual",
          "valor",
          "quântica",
          "sítio",
          "sucesso",
          "muito",
          "comida",
          "viver",
          "elfa",
          "caixa",
          "barranco",
          "dentro",
          "descer",
          "feliz",
          "ajudar",
          "arrumação",
          "executar",
          "necessidades"
        ],
        "entities": [
          [
            "valor de uma música",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "sucesso",
            "PERSON"
          ],
          [
            "faz sucesso",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "sucesso",
            "PERSON"
          ],
          [
            "valor monetário",
            "PERSON"
          ],
          [
            "jogo de xadrez",
            "ORG"
          ],
          [
            "terá consequência junto",
            "PERSON"
          ]
        ],
        "readability_score": 87.16811594202899,
        "semantic_density": 0,
        "word_count": 207,
        "unique_words": 123,
        "lexical_diversity": 0.5942028985507246
      },
      "preservation_score": 1.6922313404239855e-05
    },
    {
      "id": 1,
      "text": "com a sua namorada, Quântica começou a descer \\no barranco sentando com cautela para se \\nacostumar. Após um tempo, Quântica se sentiu \\nconfiante mas, no final do barranco, tinha uma \\nestrada de pedras e a Q uântica estava \\npreocupada em como parar ao chegar na estrada, \\nmesmo assim, ela falou: Eu vou, foda -se! \\nQuântica foi em pé, em uma velocidade que ela \\nnão esperava, pois o peso do seu corpo ficou mais \\nconcentrado e o atrito com o chão era menor que \\nsentado, fazendo ela deslizar muito rápido e \\nchegar até a estrada de pedra. Quântica, no \\nentanto, devido a sua habilidade e sagacidade, se \\nfodeu toda, arranhou o joelho, cotovelo, ficou \\ntoda arranhada, porém muito feliz em ter \\nconseguido. Ao entrar na piscina, Quân tica \\npercebeu o quanto aquela queda do papelão era \\npior do que ela esperava, pois parecia que todo o \\nseu corpo estava ardendo e realmente estava, \\ntodo arranhado, e Elfa, por sua vez, ficava \\nfalando: Você pensa que é pica das galáxias, \\nnovinha... Bem feito!  E ficaram rindo da situação \\nem que ali se encontravam, se beijando, \\nabraçando, tocando e se amando muito.  \\nQuântica e Elfa  resolveram se casar, Quântica \\nestava com 37 anos, bem resolvida na vida, \\nganhando por volta de quinze mil ao mês, \\nsatisfeita em sempre administrar o seu dinheiro, \\nmesmo quando ganhava pouco, Quântica sempre \\nsoube viver de acordo com o que ela ganhava,",
      "position": 152246,
      "chapter": 6,
      "page": 124,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.051923076923078,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 29.25,
        "avg_word_length": 4.756410256410256,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.19230769230769232,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "estava",
          "estrada",
          "muito",
          "barranco",
          "chegar",
          "mesmo",
          "esperava",
          "pois",
          "corpo",
          "ficou",
          "toda",
          "todo",
          "elfa",
          "sempre",
          "ganhava",
          "namorada",
          "começou",
          "descer",
          "sentando"
        ],
        "entities": [
          [
            "namorada",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "barranco sentando",
            "PERSON"
          ],
          [
            "cautela para se \\nacostumar",
            "PERSON"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "confiante mas",
            "PERSON"
          ],
          [
            "estrada de pedras",
            "ORG"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "Eu vou",
            "PERSON"
          ],
          [
            "ela \\nnão esperava",
            "PERSON"
          ]
        ],
        "readability_score": 83.94807692307693,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 156,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 3.2157216639965757e-05
    },
    {
      "id": 1,
      "text": "estava satisfeita em ter uma casa, comida, cama, \\ntelevisão e isso era tudo necessário para se viver \\nbem e as demais coisas. Quântica saia quando \\ndava para sair e, para reformar a sua casa, ficou \\num bom tempo indo para lugares que tivesse a \\nnecessidade de gast ar pouco dinheiro, bebendo \\nsem a necessidade de beber muito e gastar muito \\ndinheiro, impondo um limite em um viver de \\nacordo com a sua própria necessidade, porém \\nnunca deixando de ser feliz e viver o momento, \\nseja ele sentado, rolando na grama, conversando , \\nbrincando, ajudando e fazendo qualquer coisa \\nque trouxesse uma felicidade contextual, pois o \\nver um sorriso e trazer um sorriso é o movimento \\nmais puro e mais gratificante que se pode \\nconquistar e ter.  \\nQuântica e Elfa resolveram casar e fazer uma \\nfesta, ambas eram atéias e queriam ser felizes, \\npois, na concepção delas, o casamento era a \\nconquista de se unir com quem você quer viver a \\nvida toda. Quântica e Elfa fizeram uma festa à \\nfantasia, onde todos podiam se sentir à vontade \\nde comer em uma mesa cheia d e comida, se \\nservir em vários isopores espalhados cheio de \\nbebidas e, além disso tudo, tinha 3 barmen, \\ngarçons, churrasqueiro e muita música animada \\nno sítio do seu amigo médico.  \\nQuase todos que passaram em sua vida estavam \\nem seu casamento: seu pai, seu t io e o marido, \\nque virou político, anão, maconheira, casal da",
      "position": 153741,
      "chapter": 6,
      "page": 125,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.386250000000004,
      "complexity_metrics": {
        "word_count": 240,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 48.0,
        "avg_word_length": 4.620833333333334,
        "unique_word_ratio": 0.6708333333333333,
        "avg_paragraph_length": 240.0,
        "punctuation_density": 0.14166666666666666,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "quântica",
          "necessidade",
          "casa",
          "comida",
          "tudo",
          "dinheiro",
          "muito",
          "pois",
          "sorriso",
          "mais",
          "elfa",
          "festa",
          "casamento",
          "vida",
          "todos",
          "estava",
          "satisfeita",
          "cama",
          "televisão"
        ],
        "entities": [
          [
            "estava satisfeita",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "quando \\ndava para sair e",
            "PERSON"
          ],
          [
            "para reformar a sua",
            "PERSON"
          ],
          [
            "pouco dinheiro",
            "PERSON"
          ],
          [
            "muito e gastar",
            "PERSON"
          ],
          [
            "muito \\ndinheiro",
            "PERSON"
          ],
          [
            "deixando de ser",
            "PERSON"
          ],
          [
            "qualquer coisa \\nque",
            "PERSON"
          ]
        ],
        "readability_score": 74.61375,
        "semantic_density": 0,
        "word_count": 240,
        "unique_words": 161,
        "lexical_diversity": 0.6708333333333333
      },
      "preservation_score": 2.3768377516496427e-05
    },
    {
      "id": 1,
      "text": "igreja, traficante, produtora, diretor de fotografia, \\no primeiro homem de Quântica e todos aqueles \\nque Quântica e Elfa queriam que estivessem ali.  \\nQuântica, a Elfa, o tio e o namorado estavam \\nsentados à mesa conversando sobre o caminho \\ndo namorado de seu tio na política, Quântica \\nlembrava da criação do namorado. Ela lembrou \\nque ele veio de uma família formada por donos \\nde muitas quitinetes, tinham muita influência na \\ncidade em que moravam, as con dições financeiras \\neram duvidosas, porque os seus pais tinham mais \\nluxo do que aparentavam ter de dinheiro e o \\nnamorado sempre teve a melhor educação em \\nboas escolas, o meio em que ele vivia era o meio \\nda luxúria ( viço, magnificência. Segundo a \\ndoutrina cr istã, um dos sete pecados capitais. Não \\ncontrolar seus desejos. Falta de personalidade \\nperante a sua própria necessidade.): boates, \\nbebidas em excesso, carros extravagantes, festas \\nem mansões, tudo que um humano e um ser \\nhumano gostam, porém,  esses excessos  vêm com \\nexorbitantes erros, ambições, ganância, vaidade e \\na própria luxúria.  \\nA vida do namorado o fez ele ter muito network  \\nao conviver com pessoas influentes, que \\ninfluenciam muitas pessoas, levando -o a ter \\nacesso a outros políticos, esses outros polític os o \\nfizeram  enxergar como deve ser feita uma \\nvontade do povo, para fazer essas vontades do \\npovo tem que executar vontades pessoais para",
      "position": 155237,
      "chapter": 6,
      "page": 126,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.639666666666667,
      "complexity_metrics": {
        "word_count": 225,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.125,
        "avg_word_length": 5.0488888888888885,
        "unique_word_ratio": 0.6888888888888889,
        "avg_paragraph_length": 225.0,
        "punctuation_density": 0.1511111111111111,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "namorado",
          "quântica",
          "elfa",
          "muitas",
          "tinham",
          "seus",
          "meio",
          "luxúria",
          "própria",
          "humano",
          "esses",
          "pessoas",
          "outros",
          "povo",
          "vontades",
          "igreja",
          "traficante",
          "produtora",
          "diretor",
          "fotografia"
        ],
        "entities": [
          [
            "primeiro homem de Quântica",
            "PERSON"
          ],
          [
            "estivessem ali",
            "PERSON"
          ],
          [
            "namorado",
            "GPE"
          ],
          [
            "namorado de seu",
            "ORG"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "lembrava da criação",
            "PERSON"
          ],
          [
            "namorado",
            "GPE"
          ],
          [
            "veio de uma família formada",
            "ORG"
          ],
          [
            "donos \\nde muitas",
            "PERSON"
          ],
          [
            "tinham muita",
            "PERSON"
          ]
        ],
        "readability_score": 84.42283333333333,
        "semantic_density": 0,
        "word_count": 225,
        "unique_words": 155,
        "lexical_diversity": 0.6888888888888889
      },
      "preservation_score": 2.5865587297363764e-05
    },
    {
      "id": 1,
      "text": "outras pessoas em especial, virando, assim, um \\nciclo eterno de “fazer para fazer o certo junto ao \\nerro”.  \\nO namorado c omentava à mesa que seus projetos \\neram focados em melhorar a qualidade de vida \\nfamiliar, pois sem uma família estruturada, não se \\ntem base para evoluir de acordo com o seu DNA. \\nTodos nós temos uma predisposição a algo e \\nnessa predisposição temos um comport amento \\nque pode ser aproveitado se souber direcioná -lo: \\nse conseguirmos fazer as famílias terem uma \\nestrutura familiar — não passarem fome e terem \\numa casa — nós podemos fazer aquela criança ter \\numa satisfação em viver, e ter satisfação em viver \\né gozar v iver e, automaticamente, ela é \\ndirecionad a para um melhor viver.  \\n— E como você pensa em fazer isso? — Quântica \\nperguntou.  \\n— Nossa geração já vem cheia de erros, pois, para \\neu ser o político que eu sou, eu tive que cometer \\nerros para fazer uma melhoria, tud o em nossas \\nvidas tem um valor a ser pago, tudo já tem um \\nconceito estabelecido diante do meu próprio \\nviver, como você vai tirar esse caráter dessas \\npessoas? Temos que investir nas crianças, pois \\naquele que é um bom pai e uma boa mãe são \\npessoas de caráter , e pessoas de caráter aceitam \\na evolução dos filhos, aceitando a evolução dos",
      "position": 156749,
      "chapter": 6,
      "page": 127,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.27789878283152,
      "complexity_metrics": {
        "word_count": 223,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 31.857142857142858,
        "avg_word_length": 4.497757847533633,
        "unique_word_ratio": 0.6502242152466368,
        "avg_paragraph_length": 223.0,
        "punctuation_density": 0.10762331838565023,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "pessoas",
          "viver",
          "pois",
          "temos",
          "caráter",
          "familiar",
          "predisposição",
          "terem",
          "satisfação",
          "como",
          "você",
          "erros",
          "evolução",
          "outras",
          "especial",
          "virando",
          "assim",
          "ciclo",
          "eterno"
        ],
        "entities": [
          [
            "outras pessoas em",
            "PERSON"
          ],
          [
            "para fazer",
            "PERSON"
          ],
          [
            "certo",
            "NORP"
          ],
          [
            "não se",
            "PERSON"
          ],
          [
            "evoluir de acordo",
            "ORG"
          ],
          [
            "terem",
            "GPE"
          ],
          [
            "nós podemos",
            "ORG"
          ],
          [
            "aquela criança",
            "PERSON"
          ],
          [
            "ela é \\ndirecionad",
            "PERSON"
          ],
          [
            "Nossa",
            "PERSON"
          ]
        ],
        "readability_score": 82.72210121716849,
        "semantic_density": 0,
        "word_count": 223,
        "unique_words": 145,
        "lexical_diversity": 0.6502242152466368
      },
      "preservation_score": 2.0827462651372127e-05
    },
    {
      "id": 1,
      "text": "filhos os próprios filhos, irão ensinar os próprios \\npais a aceitar e viver melhor em um contexto.  \\n— E quem não é boa mãe ou bom pai, como está \\nsendo classificado nisso? — questi onou.  \\n— Todos os bons filhos são bons pais, se você tem \\nvida, você é filho de alguém. Automaticamente, \\nessa regra serve para todos aqueles que pensam \\nem amar o próximo mais que a si mesmo, essa \\nregra faz você enxergar o que é amar, pois Jesus \\ndeu a vida pa ra todos nós porque ele nos ama. \\nPadres, monges e a maioria dos líderes espirituais \\nnas religiões não podem ter um cônjuge, pois a \\nsua forma de amar tem que ser por todos, e não \\nsó para uma pessoa ou um grupo familiar.",
      "position": 158121,
      "chapter": 6,
      "page": 128,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.899479166666666,
      "complexity_metrics": {
        "word_count": 128,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 21.333333333333332,
        "avg_word_length": 4.109375,
        "unique_word_ratio": 0.7265625,
        "avg_paragraph_length": 128.0,
        "punctuation_density": 0.125,
        "line_break_count": 13,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "filhos",
          "você",
          "amar",
          "próprios",
          "pais",
          "bons",
          "vida",
          "essa",
          "regra",
          "pois",
          "irão",
          "ensinar",
          "aceitar",
          "viver",
          "melhor",
          "contexto",
          "quem",
          "como",
          "está"
        ],
        "entities": [
          [
            "irão",
            "ORG"
          ],
          [
            "ensinar",
            "PERSON"
          ],
          [
            "filho de alguém",
            "ORG"
          ],
          [
            "Automaticamente",
            "PERSON"
          ],
          [
            "essa regra serve",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "próximo mais",
            "PERSON"
          ],
          [
            "essa \\nregra",
            "ORG"
          ],
          [
            "faz você enxergar o que",
            "ORG"
          ],
          [
            "Jesus",
            "PERSON"
          ]
        ],
        "readability_score": 88.10052083333333,
        "semantic_density": 0,
        "word_count": 128,
        "unique_words": 93,
        "lexical_diversity": 0.7265625
      },
      "preservation_score": 5.954147308899207e-06
    },
    {
      "id": 1,
      "text": "Capítulo 25 sabedoria ou inteligência  \\n \\nQuântica estava voando em seu trabalho, estava \\nleve e feliz, o reconhecimento na empresa diante \\ndo seu trabalho executado fez a Quântica ganhar \\numa viagem em uma faculdade exemplar para os \\nestudos de física quântica e neurociência, essa \\nescol a estava com dificuldades em direcionar e \\nmanter os alunos da própria escola, porém, por \\nser uma escola muito renomada nessas áreas, a \\ncaptação de alunos se tornava mais difícil, devido \\na escassez desse nicho em se ter novos \\nprofissionais capacitados a apr ender essa área \\ncomplexa de necessidade, em se ter sabedoria e \\ninteligência de interpretar a si mesmo (nossos \\nporquês nos movimentam a melhorar o nosso \\npróprio viver) para um melhor entendimento da \\nprópria física quântica. Os próprios alunos, por só \\naprend erem através da inteligência, e não através \\nde viver, ficaram todos sem saber as respostas \\nbásicas de um próprio viver, pois o não viver \\nocasionava a falta de enxergar e criar novos \\nporquês diante dos próprios questionamentos.  \\nQuântica não sabia nada sobre  isso e não tinha a \\nmenor ideia de como resolveria essa questão de \\nnão entender sobre física quântica e neurociência \\ne, por isso, viu a necessidade de uma pessoa para \\ndirecioná -la melhor, essa mesma pessoa tinha \\nque entender a forma dela pensar para saber",
      "position": 159082,
      "chapter": 25,
      "page": 130,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.52511627906976,
      "complexity_metrics": {
        "word_count": 215,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 71.66666666666667,
        "avg_word_length": 5.083720930232558,
        "unique_word_ratio": 0.6372093023255814,
        "avg_paragraph_length": 215.0,
        "punctuation_density": 0.07906976744186046,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "essa",
          "viver",
          "inteligência",
          "estava",
          "física",
          "alunos",
          "sabedoria",
          "trabalho",
          "diante",
          "neurociência",
          "própria",
          "escola",
          "novos",
          "necessidade",
          "porquês",
          "próprio",
          "melhor",
          "próprios",
          "através"
        ],
        "entities": [
          [
            "25",
            "CARDINAL"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "quântica e neurociência",
            "PERSON"
          ],
          [
            "da própria",
            "PERSON"
          ],
          [
            "tornava mais difícil",
            "PERSON"
          ],
          [
            "ender essa área \\ncomplexa de necessidade",
            "PERSON"
          ],
          [
            "nos movimentam",
            "PERSON"
          ],
          [
            "física quântica",
            "PERSON"
          ],
          [
            "ficaram",
            "PERSON"
          ]
        ],
        "readability_score": 62.641550387596894,
        "semantic_density": 0,
        "word_count": 215,
        "unique_words": 137,
        "lexical_diversity": 0.6372093023255814
      },
      "preservation_score": 1.349928134811156e-05
    },
    {
      "id": 1,
      "text": "explicar e fazê -la entender o laboratório que \\nmandaram ela fazer para executar o comercial e, \\nentão, ela chamou seu amigo anão.  \\nChegando na faculdade, com uma reunião \\nmarcada com um neurocientista e um físico \\nquântico, Quântica, sempre muito esperta, \\npensa ndo sempre um passo a frente, lembrou de \\numa frase de Maquiavel: “A guerra não se evita, \\nmas apenas se adia para benefícios de outros.”  \\nPercebeu que o problema de uma empresa ou de \\nqualquer território, país e qualquer \\ndirecionamento em grande escala popula cional é \\no líder do direcionamento, que faz o restante \\nacertar ou errar. Chamou os dois líderes para \\nconversar em um lugar em que ambos ficassem \\nconfortáveis, que conseguissem sentir leveza em \\nconversar sendo eles mesmos.  \\nQuântica sentiu o peso da cobrança  no local da \\nfaculdade, tudo era muito sério, cheio de regras, \\nnada se podia fazer, pois não era coerente viver \\nde tal forma ao ser um profissional na área, a \\nimagem passada para as gerações futuras não \\nseria coerente a um viver “bom”. Chegou na sala \\npara marcar o encontro e logo percebera que os \\ndois líderes eram os culpados pela própria \\nausência de viver a vida, direcionando toda a \\nfaculdade a um estilo de vida semelhante à deles, \\nobrigando a seguir o pensamento e o estilo de um \\nviver acadêmico antigo, tr ansformando uma",
      "position": 160538,
      "chapter": 6,
      "page": 131,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 35.04009009009009,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.0,
        "avg_word_length": 4.8558558558558556,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.11261261261261261,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "faculdade",
          "fazer",
          "chamou",
          "quântica",
          "sempre",
          "muito",
          "qualquer",
          "direcionamento",
          "dois",
          "líderes",
          "conversar",
          "coerente",
          "vida",
          "estilo",
          "explicar",
          "fazê",
          "entender",
          "laboratório",
          "mandaram"
        ],
        "entities": [
          [
            "ela fazer",
            "PERSON"
          ],
          [
            "para executar",
            "PERSON"
          ],
          [
            "ela chamou",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Quântica",
            "GPE"
          ],
          [
            "muito esperta",
            "PERSON"
          ],
          [
            "lembrou de \\numa frase",
            "PERSON"
          ],
          [
            "mas apenas",
            "PERSON"
          ],
          [
            "adia",
            "ORG"
          ],
          [
            "de outros",
            "PERSON"
          ]
        ],
        "readability_score": 80.04324324324324,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 148,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 2.0248922022167342e-05
    },
    {
      "id": 1,
      "text": "geração moderna em ultrapassada, devido a não \\nenxergar a sua própria “involução” em ser feliz.  \\nQuântica teve uma ideia, levar os dois a um local \\nonde se sentiriam desconfortáveis ou à vontade, \\npropôs a seguinte coisa: vamos a uma casa de \\nstripper, se não aceitarem, não farei o trabalho.  \\n Quântica, o anão, o físico quântico e o \\nneurocientista foram, então, para a casa de \\nstripper. Ao chegar, Quântica, sempre um passo à \\nfrente, já colocou uma dose de tequila para deixar \\nos rapazes mais soltos ao se abrirem e \\nconversarem para melhor entender o problema \\nque estava ocorrendo.  \\nVocê pode me explicar o que é neurociência de \\nforma que eu consiga entender o sentimento que \\neu preciso passar para os seus futuros clientes? — \\nQuântica pede.  \\nÉ você interpre tar o viver através da matemática, \\ncompreender que a nossa mente trabalha em um \\npadrão que podemos traduzir através da \\ntecnologia, fazendo isso, conseguimos resolver os \\nproblemas antes que fiquem piores, desde curar \\numa doença que ainda não tem cura antes da \\ncriança nascer a encontrar a cura para não \\ndesenvolvermos Alzheimer no final de vida — a \\nneurocientista responde.",
      "position": 161986,
      "chapter": 6,
      "page": 132,
      "segment_type": "page",
      "themes": {
        "ciencia": 72.22222222222221,
        "tecnologia": 27.77777777777778
      },
      "difficulty": 29.985714285714288,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 4.9523809523809526,
        "unique_word_ratio": 0.6772486772486772,
        "avg_paragraph_length": 189.0,
        "punctuation_density": 0.12698412698412698,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "casa",
          "stripper",
          "neurocientista",
          "entender",
          "você",
          "através",
          "antes",
          "cura",
          "geração",
          "moderna",
          "ultrapassada",
          "devido",
          "enxergar",
          "própria",
          "involução",
          "feliz",
          "teve",
          "ideia",
          "levar"
        ],
        "entities": [
          [
            "geração moderna",
            "PERSON"
          ],
          [
            "se não aceitarem",
            "PERSON"
          ],
          [
            "Quântica",
            "PERSON"
          ],
          [
            "físico quântico e o \\nneurocientista foram",
            "PERSON"
          ],
          [
            "Quântica",
            "GPE"
          ],
          [
            "neurociência de \\nforma",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "cura",
            "ORG"
          ]
        ],
        "readability_score": 85.01428571428572,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 128,
        "lexical_diversity": 0.6772486772486772
      },
      "preservation_score": 1.6874101685139456e-05
    },
    {
      "id": 1,
      "text": "Físico quântico, o que você me diz sobre onde e \\ncomo podemos usar a física quântica em nosso \\ndia a dia? — indaga o anão.  \\n — Física quântica  está presente em tudo o que \\nexiste. Tudo é energia e física quântica, é como se \\nfosse o mundo da energia, seja ela em menor \\nescala, que seria o mundo do átomo, ou em uma \\nmaior escala, esse seria o universo em que \\nvivemos. A física quântica estuda o movime nto \\npadrão da energia em escala quântica, sendo \\nassim, para entendermos o universo, só \\nprecisamos entender o “mundo do átomo” — diz. \\n— Como posso usar isso na vida? — questiona o \\nAnão.  \\n — Pensa da seguinte forma: nós somos energia, \\ne essa energia sempre es tá no movimento de se \\npropagar, essa propagação tem um padrão de \\nmovimento, como se fossem ondas, furacões, \\ndepende da forma que usamos a analogia, nesse \\ncaso eu usarei as ondas do mar ou o efeito \\nborboleta (algo que acontece em escala \\n“pequena”, que fica muito maior do que \\nesperava), assim são os acontecimentos \\nquânticos, eles são “invisíveis” e, quando ficam \\nvisíveis, as consequências são enormes. Se nós \\nmoramos na Terra e no sistema em que o planeta \\nvive se tem um mecanismo de concordância ao se \\nmoviment ar um planeta para com o outro, a \\ngaláxia para com a outra, nós conseguimos achar",
      "position": 163258,
      "chapter": 6,
      "page": 133,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.006140350877192,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 25.333333333333332,
        "avg_word_length": 4.464912280701754,
        "unique_word_ratio": 0.6271929824561403,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.13596491228070176,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quântica",
          "energia",
          "como",
          "física",
          "escala",
          "mundo",
          "usar",
          "anão",
          "tudo",
          "seria",
          "átomo",
          "maior",
          "universo",
          "padrão",
          "assim",
          "forma",
          "essa",
          "movimento",
          "ondas",
          "planeta"
        ],
        "entities": [
          [
            "Físico quântico",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "Física",
            "PRODUCT"
          ],
          [
            "que seria o mundo",
            "ORG"
          ],
          [
            "universo em que \\nvivemos",
            "ORG"
          ],
          [
            "quântica estuda",
            "PERSON"
          ],
          [
            "para entendermos",
            "PERSON"
          ],
          [
            "universo",
            "PERSON"
          ],
          [
            "questiona",
            "PERSON"
          ]
        ],
        "readability_score": 85.99385964912281,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 143,
        "lexical_diversity": 0.6271929824561403
      },
      "preservation_score": 3.0373383033251017e-05
    },
    {
      "id": 1,
      "text": "um padrão de acontecimentos antes de suceder, \\nassim os astrólogos começaram a prever \\nacontecimentos futuros, religiões faziam as \\nmesmas coisas, tudo à nossa volta se moviment a \\nquanticamente e nós, humanos, somos \\nsemelhantes, pois se conseguirmos prever os \\nacontecimentos da nossa mente e do nosso \\ncorpo, conseguimos fazer isso quanticamente, e a \\nideia de unir a neurociência e a física quântica é \\nentender o humano em escala de co mpreender \\nque não podemos mais nos causar danos, e sim \\nviver melhor, pois conseguiríamos entender o \\ninício quântico antes que se torne energia física.  \\n— Deixa eu ver se consegui entender o que vocês \\nestão falando para um humano comum em \\ntermos de sentiment os perante a profissão de \\nvocês, quando nascemos, nós temos a \\nnecessidade de chorar e isso nos faz \\nexperimentar uma sensação dolorosa ao abrir os \\npulmões e expulsar o líquido que estava dentro \\ndeles, trocando -o por oxigênio. Esse é o primeiro \\nmovimento que  um humano precisa fazer para \\nter uma vida “normal”, após isso acontecer, \\ntemos que colocar a criança no colo da mãe para \\nela sentir confiança, pois ela ficou nove meses na \\nbarriga da mãe, devido a isso, ela já está \\nfamiliarizada com a mãe, em seguida, ama mentar \\né a primeira necessidade de se alimentar para \\nsobreviver. Vejo que o início da vida do ser",
      "position": 164653,
      "chapter": 6,
      "page": 134,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.45810810810811,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 55.5,
        "avg_word_length": 4.86036036036036,
        "unique_word_ratio": 0.6531531531531531,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.1036036036036036,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "isso",
          "acontecimentos",
          "pois",
          "entender",
          "humano",
          "antes",
          "prever",
          "nossa",
          "quanticamente",
          "fazer",
          "física",
          "início",
          "vocês",
          "temos",
          "necessidade",
          "vida",
          "padrão",
          "suceder",
          "assim",
          "astrólogos"
        ],
        "entities": [
          [
            "padrão de acontecimentos",
            "ORG"
          ],
          [
            "religiões faziam",
            "PERSON"
          ],
          [
            "mesmas coisas",
            "PERSON"
          ],
          [
            "não podemos mais",
            "ORG"
          ],
          [
            "Deixa eu",
            "PERSON"
          ],
          [
            "quando nascemos",
            "PERSON"
          ],
          [
            "nós temos",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "para \\n",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ]
        ],
        "readability_score": 70.7918918918919,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 145,
        "lexical_diversity": 0.6531531531531531
      },
      "preservation_score": 1.822402981995061e-05
    },
    {
      "id": 1,
      "text": "humano é muito mais o corpo mandando nele do \\nque a mente mandando nele — articulou o Anão.  \\nEssa mesma criança é muito mais ativa que o \\nnormal, chegando a ser hiperativa, afetando -a a \\nponto de não conseguir parar de correr, criando \\nfalta de atenção em coisas básicas e fazendo \\npouco uso de sua capacidade mental. Vejo, \\nnovamente, o corpo humano mandando no \\nhumano — continuou o Anão. — Ao chegar na \\nadolescência, es sa criança está virando adulta, \\ncheia de hormônios, cheia de energia, querendo \\nmovimentar -se igual louca, sem saber como \\ncontrolar o seu próprio corpo, tudo em sua vida é \\npensar em muitas coisas, querer fazer muitas \\ncoisas, não conseguir controlar o excess o de \\nenergia que está emergindo em seu corpo e sua \\nmente, devido a necessidade evolutiva de \\nprecisar aprender, fazendo nosso corpo, mais \\numa vez, mandar em querer sexo (todos os dias \\nacorda excitada), bebida (aumenta a vontade de \\nviver), bala (aumenta a vo ntade de viver), \\nmaconha (cria conforto na forma de viver ), \\ncomidas com um teor calórico alto, pois o corpo \\npede e qualquer coisa que é necessária para viver \\nde acordo com o estilo de vida do adolescente.  \\nEntre 20 e 30 anos nossos corpos estão no auge \\nde querer viver sexo, comida, bebida, felicidade, \\nexcessos para todos os lados de um viver e isso \\ntudo porque os nossos corpos mandam na nossa \\nvontade de fazer algo. Nessa faixa etária, a pessoa",
      "position": 166100,
      "chapter": 6,
      "page": 135,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.40246913580247,
      "complexity_metrics": {
        "word_count": 243,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 40.5,
        "avg_word_length": 4.674897119341564,
        "unique_word_ratio": 0.6172839506172839,
        "avg_paragraph_length": 243.0,
        "punctuation_density": 0.13168724279835392,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "corpo",
          "viver",
          "humano",
          "mais",
          "mandando",
          "coisas",
          "querer",
          "muito",
          "nele",
          "mente",
          "anão",
          "criança",
          "conseguir",
          "fazendo",
          "está",
          "cheia",
          "energia",
          "controlar",
          "tudo",
          "vida"
        ],
        "entities": [
          [
            "humano é muito mais o",
            "PERSON"
          ],
          [
            "corpo mandando nele",
            "PERSON"
          ],
          [
            "mandando nele",
            "PERSON"
          ],
          [
            "Anão",
            "ORG"
          ],
          [
            "muito mais ativa",
            "PERSON"
          ],
          [
            "pouco uso de sua",
            "PERSON"
          ],
          [
            "Vejo",
            "GPE"
          ],
          [
            "Anão",
            "ORG"
          ],
          [
            "querer fazer",
            "PERSON"
          ],
          [
            "nosso corpo",
            "PERSON"
          ]
        ],
        "readability_score": 78.34753086419752,
        "semantic_density": 0,
        "word_count": 243,
        "unique_words": 150,
        "lexical_diversity": 0.6172839506172839
      },
      "preservation_score": 3.145814671300998e-05
    },
    {
      "id": 1,
      "text": "que tem muita energia corpórea, controlar esses \\nimpulsos requer muita energia mental, nos \\ntransformando, mais uma vez, em escravos do \\nnosso próprio corpo.  \\nEntre os 30 e os 40 anos é o meio da idade do \\nhumano (um metabolismo padrão de um corpo \\nhumano padrão só começa a cair aos 60 anos), \\nquando chega essa faixa etária,  começamos a \\nsentir os nossos corpos mais cansados, as nossas \\ntaxas hormonais começam a ficar instáveis, \\nnossos corpos já estão vindo cansados de um \\nviver muitas coisas, queremos construir um \\nfuturo melhor, mas isso não acontece de uma \\nforma fácil, devido a  um viver sem perceber o \\npreço que pagamos ao viver. Os nossos corpos \\nficando mais cansados, automaticamente, as \\nnossas mentes também ficam mais cansadas, \\nnossa mente e o corpo mais cansados não \\nconseguimos assimilar um viver melhor diante do \\nnosso próprio  cansaço, o que acarreta crises de \\nansiedade, existencial, cobrança, depressão, \\nindecisões, conflitos, querer viver e não ter forças \\npara viver aquilo que tem vontade, o nosso corpo \\nmanda novamente em nossa mente, devido a não \\nter forças para fazer o que v ocê quer fazer, sonha \\nem fazer, porém o nosso corpo cansado não nos \\ndeixa fazer, toda a nossa vida nessa faixa etária é \\numa briga de querer e não conseguir e, se fizer, \\npaga um preço que não pode pagar, devido as \\nobrigações de sustentar -se (viver o excesso  o",
      "position": 167626,
      "chapter": 6,
      "page": 136,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.44439655172414,
      "complexity_metrics": {
        "word_count": 232,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 77.33333333333333,
        "avg_word_length": 4.814655172413793,
        "unique_word_ratio": 0.6206896551724138,
        "avg_paragraph_length": 232.0,
        "punctuation_density": 0.1336206896551724,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "mais",
          "corpo",
          "nosso",
          "cansados",
          "fazer",
          "nossos",
          "corpos",
          "devido",
          "nossa",
          "muita",
          "energia",
          "próprio",
          "anos",
          "humano",
          "padrão",
          "faixa",
          "etária",
          "nossas",
          "melhor"
        ],
        "entities": [
          [
            "impulsos requer",
            "PERSON"
          ],
          [
            "40",
            "CARDINAL"
          ],
          [
            "meio da",
            "PERSON"
          ],
          [
            "humano padrão",
            "PERSON"
          ],
          [
            "só começa",
            "PERSON"
          ],
          [
            "60",
            "CARDINAL"
          ],
          [
            "quando chega",
            "PERSON"
          ],
          [
            "nossas \\ntaxas",
            "PERSON"
          ],
          [
            "mais cansadas",
            "PERSON"
          ],
          [
            "cobrança",
            "ORG"
          ]
        ],
        "readability_score": 59.888936781609196,
        "semantic_density": 0,
        "word_count": 232,
        "unique_words": 144,
        "lexical_diversity": 0.6206896551724138
      },
      "preservation_score": 2.4467447443452205e-05
    },
    {
      "id": 1,
      "text": "engorda, fica fácil), comprar uma casa, cuidar da \\nfamília, carro, melhorar o seu viver, melhorar a \\nvida para um próprio viver melhor na maior \\nidade.  \\nEntre 40 e 50 anos ocorre a transição de aceitar \\nos seus conflitos a não ter conflitos. Nessa idade, \\ncom eçamos a perceber que a guerra não \\ncompensa o gasto de energia, aprendemos a \\nentender que o viver não é brigar, criticar, \\nreclamar, planejar, querer tantas coisas que nada \\nvai pagar o tempo que se perde achando que um \\nviver melhor era a tal coisa. Aqui com eçamos a \\nentender que os nossos corpos não têm mais \\ncomo mandar em nós.  \\nEntre 50 e 60 anos é idade que melhor se vive, de \\nacordo com as pesquisas. É a idade que todo \\nmundo liga o foda -se, a faixa etária que mais \\naceita a própria idade, faz o que consegue e  o que \\nnão consegue, aceita e fica satisfeito por estar \\nvivo. É a faixa etária que compreendemos que os \\nnossos corpos são falhos e a nossa mente sabe \\nnos guiar melhor que os nossos corpos, o \\nmovimentar -se menos nos faz pensar em como se \\nmovimentar melhor; nem sempre temos que ter \\no excesso de  trabalho, bebida, comida, qualquer \\ncoisa que prejudicará o tempo de parar e pensar \\nem como melhorar o nosso próprio viver, vivemos \\ntão intensamente que esquecemos de pensar \\ncomo se viver melhor. Nessa idade o corpo não  \\nnos permite fazer muitas coisas,",
      "position": 169125,
      "chapter": 6,
      "page": 137,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 30.608057851239668,
      "complexity_metrics": {
        "word_count": 242,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 30.25,
        "avg_word_length": 4.433884297520661,
        "unique_word_ratio": 0.5661157024793388,
        "avg_paragraph_length": 242.0,
        "punctuation_density": 0.12396694214876033,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "melhor",
          "idade",
          "como",
          "melhorar",
          "nossos",
          "corpos",
          "pensar",
          "fica",
          "próprio",
          "entre",
          "anos",
          "conflitos",
          "nessa",
          "eçamos",
          "entender",
          "coisas",
          "tempo",
          "coisa",
          "mais"
        ],
        "entities": [
          [
            "engorda",
            "ORG"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "casa",
            "GPE"
          ],
          [
            "cuidar da \\nfamília",
            "PERSON"
          ],
          [
            "melhorar o seu",
            "ORG"
          ],
          [
            "40 e",
            "CARDINAL"
          ],
          [
            "Nessa",
            "PERSON"
          ],
          [
            "nada \\nvai pagar o",
            "ORG"
          ],
          [
            "que se perde achando",
            "ORG"
          ],
          [
            "50 e",
            "CARDINAL"
          ]
        ],
        "readability_score": 83.5448347107438,
        "semantic_density": 0,
        "word_count": 242,
        "unique_words": 137,
        "lexical_diversity": 0.5661157024793388
      },
      "preservation_score": 2.306930758954065e-05
    },
    {
      "id": 1,
      "text": "automaticamente nossa mente acha atalhos para \\nse viver melhor.  \\n— Tenho um pensamento sobre buraco negro \\nque é “semelhante” — emendou o físico \\nquântico.  É um pensamento sobre o que ocorre \\ndentro de um buraco negro, eu vejo  que a física é \\na teoria da matéria e a física Quântica é a teoria \\nda energia, o buraco negro, a meu ver , é como se \\nfosse um furacão de areia. Toda galáxia tem um \\nburaco negro no centro dela, no entorno estão as \\nmatérias físicas (asteroides, poeira cósmic a, \\nplanetas, estrelas etc. ). Quando essa matéria \\nfísica atinge a velocidade acima da velocidade da \\nluz, se transforma tudo em energia quântica, \\nassemelhando -se a nossas memórias \\n(entrelaçamento quântico), só energia na mente \\nao ser canalizada e pensada, os nossos corpos \\nfísicos transformam aquela energia quântica em \\nenergia física (mundo real). Semelhante a um \\nburaco negro que concentra a matéria física, essa \\nmesma matéria física vai acumulando dentro do \\nseu próprio corpo quântico, até o ponto que o \\nprópr io corpo não aguenta absorver mais energia, \\nexpelindo em forma de quasar e criando novas \\ngaláxias, sistemas, planetas e tudo que se pode \\nter em um universo.  \\nOs assuntos são muito complexos, e eu não sou \\nexpert, porém me deixa  tentar fazer a ligação \\nentre o s três assuntos — articula Quântica. — A \\nmente humana é o mundo quântico. Nossos",
      "position": 170590,
      "chapter": 6,
      "page": 138,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.8910480349345,
      "complexity_metrics": {
        "word_count": 229,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 22.9,
        "avg_word_length": 4.8034934497816595,
        "unique_word_ratio": 0.6462882096069869,
        "avg_paragraph_length": 229.0,
        "punctuation_density": 0.1222707423580786,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "física",
          "energia",
          "buraco",
          "negro",
          "quântico",
          "matéria",
          "quântica",
          "mente",
          "pensamento",
          "semelhante",
          "dentro",
          "teoria",
          "planetas",
          "essa",
          "velocidade",
          "tudo",
          "nossos",
          "mundo",
          "corpo",
          "assuntos"
        ],
        "entities": [
          [
            "automaticamente nossa mente acha atalhos",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "eu vejo",
            "PERSON"
          ],
          [
            "teoria da matéria",
            "PERSON"
          ],
          [
            "Quântica",
            "NORP"
          ],
          [
            "buraco negro",
            "ORG"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "poeira cósmic",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ]
        ],
        "readability_score": 87.1089519650655,
        "semantic_density": 0,
        "word_count": 229,
        "unique_words": 148,
        "lexical_diversity": 0.6462882096069869
      },
      "preservation_score": 2.8661867005186868e-05
    },
    {
      "id": 1,
      "text": "corpos são o mundo da física. O estudar essas \\ncoisas os fez ficar sem perceber o próprio erro, \\ndevido a vocês estarem muito perto do problema, \\nnão conseguiram entender o lado humano do \\nestudo, o viver é saber movimentar -se. Nós \\ntemos que nos movimentar de uma forma em \\nque a nossa mente e o nosso corpo tenham \\nequilíbrio na nossa energia (metabolismo), para \\nconseguimos viver felizes, temos que aprender a \\ndoutrinar nossos impulsos  (histeria, desejos \\nprimitivos) corpóreos através da nossa mente.  \\nNa evolução humana, tivemos muitas diferenças \\ncomportamentais, essas diferenças nos fizeram \\ncriar sentimentos pelo semelhante, a minha dor \\nou felicidade, tudo que somos é devido a \\nvivermos e  aprendermos que a nossa felicidade \\nou o nosso caos é semelhante ao das pessoas à \\nminha volta, ou se eu não vivi com muitas \\npessoas à minha volta, a minha vida será \\nsemelhante ao que eu leio, vejo e estudo.  \\nA miséria é o impulso da igreja pela falta de um \\nviver bem e a semelhança com o caos de um viver \\nruim.  \\nNós somos atraídos pela semelhança de um viver, \\nse vivermos de uma forma semelhante a um \\npolítico, como seremos?  \\nTraficante, como seremos?  \\nMulher, como seremos?",
      "position": 172069,
      "chapter": 6,
      "page": 139,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.831060606060607,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 24.75,
        "avg_word_length": 4.853535353535354,
        "unique_word_ratio": 0.6111111111111112,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.12626262626262627,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "nossa",
          "semelhante",
          "minha",
          "como",
          "seremos",
          "essas",
          "devido",
          "estudo",
          "movimentar",
          "temos",
          "forma",
          "mente",
          "nosso",
          "muitas",
          "diferenças",
          "felicidade",
          "somos",
          "vivermos",
          "caos"
        ],
        "entities": [
          [
            "corpos são o mundo da física",
            "ORG"
          ],
          [
            "fez ficar sem perceber",
            "PERSON"
          ],
          [
            "estarem muito",
            "PERSON"
          ],
          [
            "lado humano",
            "PERSON"
          ],
          [
            "impulsos",
            "PERSON"
          ],
          [
            "desejos \\nprimitivos",
            "PERSON"
          ],
          [
            "tivemos muitas",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "se eu não vivi",
            "PERSON"
          ],
          [
            "que eu leio",
            "PERSON"
          ]
        ],
        "readability_score": 86.1689393939394,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 121,
        "lexical_diversity": 0.6111111111111112
      },
      "preservation_score": 1.9525746235661365e-05
    },
    {
      "id": 1,
      "text": "Homossexual, como seremos?  \\nHomem, como seremos?  \\nComo seríamos se vivêssemos na Palestina no \\ntempo de Cristo?  \\nComo seríamos felizes vivendo na Palestina?  \\nQual seria o maior exemplo de ser quem eu \\ndeveria ser?  \\nSe sofrêssemos semelhantes ao Moisés, Paulo, \\nDaniel, Jesus qual seria a nossa maio r \\nrecompensa?  \\nSe olharmos para os nossos exemplos, esses \\nmesmos exemplos atingiram a maior conquista \\nque podemos alcançar através da dor, pois, \\natravés dessa mesma dor, obtemos a nossa maior \\nconquista de um viver: o direito de encontrar \\nDeus, o mesmo Deus que você só encontra ao \\nmorrer.  \\nA maior conquista que um humano pode ter é a \\nprópria morte.",
      "position": 173379,
      "chapter": 7,
      "page": 140,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.133490566037736,
      "complexity_metrics": {
        "word_count": 106,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 13.25,
        "avg_word_length": 5.028301886792453,
        "unique_word_ratio": 0.7452830188679245,
        "avg_paragraph_length": 106.0,
        "punctuation_density": 0.1792452830188679,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "maior",
          "conquista",
          "seremos",
          "seríamos",
          "palestina",
          "qual",
          "seria",
          "nossa",
          "exemplos",
          "através",
          "deus",
          "homossexual",
          "homem",
          "vivêssemos",
          "tempo",
          "cristo",
          "felizes",
          "vivendo",
          "exemplo"
        ],
        "entities": [
          [
            "seremos",
            "PERSON"
          ],
          [
            "Homem",
            "PERSON"
          ],
          [
            "seremos",
            "PERSON"
          ],
          [
            "de Cristo",
            "ORG"
          ],
          [
            "Palestina",
            "PERSON"
          ],
          [
            "seria o maior",
            "ORG"
          ],
          [
            "quem eu",
            "PERSON"
          ],
          [
            "Moisés",
            "ORG"
          ],
          [
            "Paulo",
            "PERSON"
          ],
          [
            "Daniel",
            "PERSON"
          ]
        ],
        "readability_score": 91.86650943396226,
        "semantic_density": 0,
        "word_count": 106,
        "unique_words": 79,
        "lexical_diversity": 0.7452830188679245
      },
      "preservation_score": 8.244203966168133e-06
    },
    {
      "id": 1,
      "text": "Capítulo 2 6 o final do início  \\nQuântica estava em seu trabalho em mais um dia \\nnormal, brincando, sorrindo, até que o seu \\ntelefone tocou. Quântica recebeu a notícia que o \\nseu pai tinha acabado de infartar e estava indo \\nem direção ao hospital. Quântica saiu correndo \\ndo seu trabalho para ir ao encontro de seu pai. Ao \\nchegar no hospital, logo veio um médico em sua \\ndireção para falar que o seu pai a estava \\nesperando em se u quarto. Ao entrar no quarto, \\nQuântica se sentou  em uma cadeira ao lado da \\ncama, pegou nas mãos de seu pai, olhou em seus \\nolhos e falou para ele: Vai dar tudo certo!  \\nSeu pai, bem debilitado e cansado, pois a idade já \\nestava bem avançada, olhou para a Quântic a e \\ndisse: Preste atenção ao que eu tenho para falar, \\npois sinto a sua vida ligada à minha desde o \\nmomento em que você nasceu, sua mãe e eu \\nsabíamos que você tinha algo diferente e não \\nentendíamos, hoje eu a vejo como você é de \\nverdade e entendo por qual m otivo você veio, \\nvejo você e consigo enxergar. Hoje, ao olhar para \\nvocê próximo de morrer, vejo a sua verdadeira \\nmissão de vida, pois você minha filha, Quântica, \\nveio viver uma vida para aprender com os erros \\ndos humanos para poder ensinar ao próprio \\nhuman o. \\n— Minha filha, você não é apenas minha filha ou \\nda sua mãe, você é filha do planeta Terra o seu",
      "position": 174325,
      "chapter": 2,
      "page": 142,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.5778,
      "complexity_metrics": {
        "word_count": 250,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 31.25,
        "avg_word_length": 4.176,
        "unique_word_ratio": 0.588,
        "avg_paragraph_length": 250.0,
        "punctuation_density": 0.12,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "quântica",
          "estava",
          "minha",
          "filha",
          "veio",
          "pois",
          "vida",
          "vejo",
          "trabalho",
          "tinha",
          "direção",
          "hospital",
          "falar",
          "quarto",
          "olhou",
          "hoje",
          "capítulo",
          "final",
          "início"
        ],
        "entities": [
          [
            "2 6",
            "DATE"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "sorrindo",
            "GPE"
          ],
          [
            "acabado de infartar e estava",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "médico em sua \\ndireção",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Quântica",
            "PRODUCT"
          ],
          [
            "nas mãos de seu",
            "PERSON"
          ],
          [
            "olhou",
            "GPE"
          ]
        ],
        "readability_score": 83.12219999999999,
        "semantic_density": 0,
        "word_count": 250,
        "unique_words": 147,
        "lexical_diversity": 0.588
      },
      "preservation_score": 2.092388608957292e-05
    },
    {
      "id": 1,
      "text": "sentimento de sentir tudo à sua volta vem de \\nsentir o mal que fazemos um para o outro e, \\ninvoluntariamente, o nosso próprio planeta Terra \\nsofre as consequênc ias devido à ganância e os \\nerros do próprio humano, você foi gerada através \\nda adaptação da energia da minha família e a \\nenergia da família de sua mãe, nós tínhamos uma \\nvida totalmente diferente um do outro, no termo \\nde sermos eu europeu, e ela negra, mas nossas \\nfamílias tinham algo em comum, nós não \\ntínhamos julgamentos, nem diferenças por \\nsermos “diferentes”, e essa junção canalizou uma \\nenergia tão correta a um estilo de viver que sua \\nenergia foi canalizada para a nossa filha que ia \\nnascer morta, nos traz endo a nossa maior perda e \\no nosso maior ganho de um viver uma vida digna, \\nvocê iluminou a minha estrada da vida em todo o \\npercurso que eu percorri, e agora, no final de \\nvida, não está sendo diferente, pois, ao olhar para \\nvocê, eu vejo o quão iluminando e abençoado eu \\nfui, pois não entendo o motivo de tanta benção \\nem ter você na minha vida, tudo que eu fiz foi \\ntudo aquilo que eu queria que fizesse por mim \\nmesmo.  \\nO pai de Quântica faleceu e, quando ele morreu, \\nQuântica desapareceu...  \\nQuântica era a energia d o senhor preconceito \\nquântico dentro de um corpo físico morto, o \\nalimento dessa canalização de energia vinha de",
      "position": 175766,
      "chapter": 7,
      "page": 143,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.347457627118644,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 78.66666666666667,
        "avg_word_length": 4.491525423728813,
        "unique_word_ratio": 0.6101694915254238,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.11440677966101695,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "vida",
          "você",
          "tudo",
          "minha",
          "quântica",
          "sentir",
          "outro",
          "nosso",
          "próprio",
          "família",
          "tínhamos",
          "diferente",
          "sermos",
          "viver",
          "nossa",
          "maior",
          "pois",
          "sentimento",
          "volta"
        ],
        "entities": [
          [
            "sentimento de sentir",
            "ORG"
          ],
          [
            "vem de \\n",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "próprio humano",
            "PERSON"
          ],
          [
            "família de sua mãe",
            "ORG"
          ],
          [
            "ela negra",
            "PERSON"
          ],
          [
            "mas nossas",
            "PERSON"
          ],
          [
            "nem diferenças",
            "PERSON"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "canalizada",
            "ORG"
          ]
        ],
        "readability_score": 59.31920903954802,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 144,
        "lexical_diversity": 0.6101694915254238
      },
      "preservation_score": 1.9573957954761764e-05
    },
    {
      "id": 1,
      "text": "seu pai e sua mãe, como se fosse uma captação \\nde uma frequência sem ruídos.  \\nAo “morrer”, o corpo de Quântica ficou em \\nestado de morte cerebral, vegetativo e sem vida!  \\nO senhor preconceito Quântico voltou ao seu \\nestado quântico, com todas as respostas sem \\nrespostas, porém com compreendendo todas as \\nrespostas que ele desconhecia. Quântico \\npercebeu que tanto ele quanto o ser humano não \\nsabiam viver e m uma energia correta, pois a \\nminha energia só existe devido ao movimento e o \\nmeu próprio movimento causa uma ação e reação \\nde mover -se, expandir e adaptar, mover -se, \\nexpandir e adaptar, em um ciclo “infinito”, na \\nevolução do próprio movimento.  \\nEm toda exi stência do ser humano, esses 200 mil \\nanos vêm de uma evolução “errada” perante a se \\nadaptar ao próprio movimento criado por nós \\nmesmos. Nossos corpos vêm em um processo de \\nadaptação, de acordo com a nossa própria \\nevolução de conforto para o nosso próprio \\nmovimento. Nossos corpos vão se adaptando de \\nacordo com a nossa própria evolução, com um \\nperíodo de adaptação proporcional ao me smo, \\neles são uma espécie nova no processo evolutivo \\nde se adaptar ao próprio movimento; dentro \\ndesses movimentos, criam características \\nevolutivas necessárias, eles usam tato para saber \\nse está quente ou frio, paladar para saber se",
      "position": 177208,
      "chapter": 7,
      "page": 144,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.90218253968254,
      "complexity_metrics": {
        "word_count": 216,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 30.857142857142858,
        "avg_word_length": 4.912037037037037,
        "unique_word_ratio": 0.6203703703703703,
        "avg_paragraph_length": 216.0,
        "punctuation_density": 0.11574074074074074,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "próprio",
          "adaptar",
          "evolução",
          "quântico",
          "respostas",
          "estado",
          "todas",
          "humano",
          "energia",
          "mover",
          "expandir",
          "nossos",
          "corpos",
          "processo",
          "adaptação",
          "acordo",
          "nossa",
          "própria",
          "eles"
        ],
        "entities": [
          [
            "seu pai e sua mãe",
            "ORG"
          ],
          [
            "de Quântica",
            "GPE"
          ],
          [
            "Quântico",
            "PERSON"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "evolução de conforto para o",
            "ORG"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "evolutivas necessárias",
            "PERSON"
          ],
          [
            "usam tato para",
            "PERSON"
          ],
          [
            "paladar",
            "ORG"
          ]
        ],
        "readability_score": 83.09781746031746,
        "semantic_density": 0,
        "word_count": 216,
        "unique_words": 134,
        "lexical_diversity": 0.6203703703703703
      },
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "id": 1,
      "text": "podem comer, ou mesmo g ostar ou não, olfato \\npara saber se estão próximos a algum perigo, \\nolhos para compreender um ao outro ou mostrar \\no amor antes mesmo de tocar. Seus movimentos \\nsão involuntários e, através do próprio \\nmovimento, descobrem o caráter, esse caráter \\nvem de caracte rísticas do DNA junto ao meio em \\nque vive, criando impulsos sentimentais \\ninvoluntários, devido a evolução familiar e \\nestrutural, gerando movimentos bruscos e, assim, \\numa maior energia para se conter, fazendo, \\nportanto, sair de um controle de contenção. Ess e \\nmovimento de conter o próprio movimento gera \\nproblemas, feridas, mágoas, lacunas e não \\nsabemos até que ponto isso nos atinge. O \\nhumano, por não aceitar o aprender, ouvir, \\nobservar, concentrar, aceitar um direcionamento \\nque outro ser humano possa pensar, como em \\norientar o melhor direcionamento, mesmo sendo \\numa direção melhor que o humano está \\nseguindo, saberia que qualquer raciocínio em que \\nvocê se colocasse no lugar do outro, conseguiria \\nenxergar e observar o seu próprio erro.  \\nOs erros deles vêm da própr ia regra gerada \\ndevido à necessidade das próprias regras.  \\nAs regras por si só são preconceituosas. As regras \\nforam criadas para conter o próprio movimento, e \\no movimento veio junto com a origem da energia.",
      "position": 178632,
      "chapter": 7,
      "page": 145,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.1823693379791,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.285714285714285,
        "avg_word_length": 5.131707317073171,
        "unique_word_ratio": 0.7024390243902439,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.16585365853658537,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "próprio",
          "mesmo",
          "outro",
          "conter",
          "humano",
          "regras",
          "movimentos",
          "involuntários",
          "caráter",
          "junto",
          "devido",
          "energia",
          "aceitar",
          "observar",
          "direcionamento",
          "melhor",
          "podem",
          "comer",
          "ostar"
        ],
        "entities": [
          [
            "algum perigo",
            "PERSON"
          ],
          [
            "mostrar \\no amor",
            "ORG"
          ],
          [
            "mesmo de tocar",
            "PERSON"
          ],
          [
            "descobrem",
            "PERSON"
          ],
          [
            "vem de caracte",
            "PERSON"
          ],
          [
            "bruscos",
            "GPE"
          ],
          [
            "para se conter",
            "PERSON"
          ],
          [
            "feridas",
            "GPE"
          ],
          [
            "mágoas",
            "GPE"
          ],
          [
            "lacunas e não \\nsabemos até que",
            "PERSON"
          ]
        ],
        "readability_score": 83.8176306620209,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 144,
        "lexical_diversity": 0.7024390243902439
      },
      "preservation_score": 2.2129179067082882e-05
    },
    {
      "id": 1,
      "text": "Capítulo 2 7 conclusão inconclusiva  \\nA falta de foc o é a própria preservação do \\nmesmo!” O estar em foco resulta da nossa \\nobservação, nossas prioridades e a nossa forma \\nde interpretar um viver emergem da nossa \\nprópria vida, e nosso aprendizado de um contexto \\nvem da nossa própria memória, e nossas \\nmemórias d erivam dê uma vivência que nós \\nmesmos interpretamos de acordo com o meio em \\nque vivemos, e esse momento que vivemos são \\nimportantes em um contexto de interpretação de \\nnós mesmos. Quando vivenciamos algo, nós \\ntemos um padrão de foco de acordo com a nossa \\nprópria necessidade de ter ou ser.  \\nTer algo é o mundo físico da nossa interpretação.  \\nSer algo é o nosso mundo espiritual.  \\nDeus fez o mundo distante dele para poder \\ninterpretar melhor, tanto o homem quanto a \\nmulher tem um padrão de ser como “deve ser”, \\nos hom ens, em sua evolução, eram “caçadores”, \\nsendo assim, o seu próprio corpo se adaptou de \\nacordo com a sua necessidade, o fazendo \\ndistribuir a sua energia corpórea de acordo com \\nessa necessidade, o homem, para suprir a sua \\nprópria necessidade evolutiva, a sua  própria \\nevolução, se encarregou de adaptar a sua \\nquantidade de neurônios de acordo com sua \\nnecessidade corpórea, fazendo os homens terem",
      "position": 180037,
      "chapter": 2,
      "page": 146,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.430647709320695,
      "complexity_metrics": {
        "word_count": 211,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 35.166666666666664,
        "avg_word_length": 4.758293838862559,
        "unique_word_ratio": 0.5734597156398105,
        "avg_paragraph_length": 211.0,
        "punctuation_density": 0.10426540284360189,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "própria",
          "nossa",
          "acordo",
          "necessidade",
          "algo",
          "mundo",
          "foco",
          "nossas",
          "interpretar",
          "nosso",
          "contexto",
          "mesmos",
          "vivemos",
          "interpretação",
          "padrão",
          "homem",
          "evolução",
          "fazendo",
          "corpórea",
          "capítulo"
        ],
        "entities": [
          [
            "2 7",
            "CARDINAL"
          ],
          [
            "própria vida",
            "PERSON"
          ],
          [
            "mesmos interpretamos de acordo",
            "PERSON"
          ],
          [
            "Quando vivenciamos",
            "PERSON"
          ],
          [
            "padrão de foco de acordo",
            "ORG"
          ],
          [
            "físico da nossa",
            "PERSON"
          ],
          [
            "interpretar melhor",
            "ORG"
          ],
          [
            "tanto o homem quanto",
            "ORG"
          ],
          [
            "para suprir a sua \\nprópria",
            "PERSON"
          ],
          [
            "encarregou de adaptar",
            "ORG"
          ]
        ],
        "readability_score": 80.9891785150079,
        "semantic_density": 0,
        "word_count": 211,
        "unique_words": 121,
        "lexical_diversity": 0.5734597156398105
      },
      "preservation_score": 1.757317161209523e-05
    },
    {
      "id": 1,
      "text": "menos neurônios e mais energia para terem um \\nmetabolismo mais forte.  \\nA mulher, por sua vez, era a “dona de casa”, as \\nmulheres eram o “pilar da família”, cuidavam das \\ncrianças, fogo, alimentação, casa, assim fazendo a \\nprópria evolução ser direcionada em ter mais \\nneurônios e menos força corpórea.  \\nQuanto tempo temos de “evolução” para nos \\nadaptarmos em sermos “homens e mulhe res”?  \\nNossa evolução de “necessidade” muda e, \\nautomaticamente, nosso corpo e nossa mente \\ntambém. Até que ponto nosso corpo e nossa \\nmente primitiva evoluíram de acordo com a nossa \\nprópria necessidade? Nosso foco em um viver é \\ntão primitivo que nós julgamos tudo e a todos \\ndevido a nossa própria evolução. Sexo, amor, \\ncostumes, religião, regras, nos transformaram em \\num ser “involuído”, impulsivo, de julgamentos \\nprimitivos ao interpretar uma imagem, corpo, \\nação, palavras, religião, como nada de \\n“sobrevivência”. Quando julgamos algo, julgamos \\ncom base em algo, esse mesmo algo vem com \\npreconceitos, esses preconceitos vêm com pesos \\nda nossa própria vivência, essa vivência vem de \\num pensamento, esse pensamento vem de você \\nmesmo, se esse pensamento junto a nossas ações \\ncorpóreas advém  de nós mesmos, por que \\njulgamos o outro sem saber o trajeto do \\npensamento e da ação do outro? Nós",
      "position": 181400,
      "chapter": 7,
      "page": 147,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.88480392156863,
      "complexity_metrics": {
        "word_count": 204,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.666666666666668,
        "avg_word_length": 5.171568627450981,
        "unique_word_ratio": 0.6715686274509803,
        "avg_paragraph_length": 204.0,
        "punctuation_density": 0.18137254901960784,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "própria",
          "evolução",
          "julgamos",
          "pensamento",
          "mais",
          "nosso",
          "corpo",
          "algo",
          "esse",
          "menos",
          "neurônios",
          "casa",
          "necessidade",
          "mente",
          "religião",
          "ação",
          "mesmo",
          "preconceitos",
          "vivência"
        ],
        "entities": [
          [
            "para terem",
            "PERSON"
          ],
          [
            "por sua vez",
            "ORG"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "Nossa",
            "PERSON"
          ],
          [
            "nosso corpo",
            "PERSON"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nada de \\n“",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "essa vivência vem de",
            "PERSON"
          ]
        ],
        "readability_score": 87.11519607843137,
        "semantic_density": 0,
        "word_count": 204,
        "unique_words": 137,
        "lexical_diversity": 0.6715686274509803
      },
      "preservation_score": 3.442316743768448e-05
    },
    {
      "id": 1,
      "text": "interpretamos aquilo que queremos interpretar, \\nnossas ações, nossas palavras, atitudes origina -se \\nda nossa própria mente.  \\nO que é um viver?  \\nO que é energia?  \\nO que é uma vida?  \\nO que é sentimento?  \\nPor que estudamos?  \\nTudo em nossa vida tem um motivo de acontecer \\ndevido a ligação involuntária dos nossos \\nmovimentos colidirem em uma escala atômica, \\ntoda a nossa vida é ligada a uma cadeia de \\npessoas que já existiram, que existem e vão \\nexistir, tudo em nossa vida só vivemos porque \\nexistimos, entrando em um ciclo infinito de \\npropagação contínua e “infinita” de energia, com \\nciclos “infinitos” de aprendizado coletivo de \\nacordo com uma predisposição  de linha de tempo \\n(DNA, dom) adaptável a necessidade ao meio em \\nque vive.  \\nOs nossos pensamentos trabalham \\nquanticamente e os nossos corpos físicos são a \\nevolução quântica, assim como os nossos corpos \\nfísicos foram gerados através do movimento, \\ntudo que ex iste e sabemos que existe é energia.",
      "position": 182807,
      "chapter": 7,
      "page": 148,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.308678343949044,
      "complexity_metrics": {
        "word_count": 157,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 19.625,
        "avg_word_length": 4.987261146496815,
        "unique_word_ratio": 0.6496815286624203,
        "avg_paragraph_length": 157.0,
        "punctuation_density": 0.12101910828025478,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "vida",
          "nossos",
          "energia",
          "tudo",
          "nossas",
          "corpos",
          "físicos",
          "interpretamos",
          "aquilo",
          "queremos",
          "interpretar",
          "ações",
          "palavras",
          "atitudes",
          "origina",
          "própria",
          "mente",
          "viver",
          "sentimento"
        ],
        "entities": [
          [
            "interpretamos",
            "PERSON"
          ],
          [
            "que queremos interpretar",
            "PERSON"
          ],
          [
            "nossas ações",
            "PERSON"
          ],
          [
            "nossas palavras",
            "PERSON"
          ],
          [
            "infinito de \\npropagação contínua e",
            "ORG"
          ],
          [
            "trabalham \\nquanticamente",
            "PERSON"
          ]
        ],
        "readability_score": 88.69132165605096,
        "semantic_density": 0,
        "word_count": 157,
        "unique_words": 102,
        "lexical_diversity": 0.6496815286624203
      },
      "preservation_score": 1.5042056359324311e-05
    },
    {
      "id": 1,
      "text": "Como todo movimento cria uma ação, esse \\nmesmo movimento cria uma reação de \\nadaptação, com uma ação de resposta “infinita”, \\naté ocorrer uma adaptação evolutiva que advém \\nde nós mesmos, em uma concordância de \\ntamanho prop orcional ao movimento.  \\nAté que ponto, sendo parcial, você conseguirá \\nsegurar o movimento da ação?  \\nEssa omissão (parcial) de não reagir, o faz \\nconcentrar sentimentos (energia) em que muitas \\nvezes uma reação faz -se necessária para conter a \\nenergia do outro m ovimento (sentimento).  \\nO excesso de movimento desencadeará uma \\nmaior contenção da própria energia, gerando \\numa maior propagação do movimento, criando \\num desgaste maior de energia para conter o \\npróprio movimento. O excesso de problemas ou o \\nexcesso de felic idade causa exaustão corpórea, \\nqualquer ação de si mesmo tem um movimento e \\num gasto de energia, nossos corpos contêm uma \\nquantidade de energia, e essa mesma energia é \\ndividida em DNA, órgãos, hormônios, tempo e \\noutros componentes que consumem o nosso \\nmeta bolismo, tudo afetando um ao outro \\nproporcionalmente ao seu estilo de vida, se \\nvivemos muitos exageros: sentimos nossos corpos \\ncriando caos dentro dele mesmo na forma de \\ncontenção dos mesmos; se ficamos com febre, \\nnossas células ficam mais agitadas gerando  mais",
      "position": 183896,
      "chapter": 7,
      "page": 149,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.571641791044776,
      "complexity_metrics": {
        "word_count": 201,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 40.2,
        "avg_word_length": 5.2388059701492535,
        "unique_word_ratio": 0.6517412935323383,
        "avg_paragraph_length": 201.0,
        "punctuation_density": 0.11940298507462686,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "energia",
          "ação",
          "mesmo",
          "excesso",
          "maior",
          "cria",
          "reação",
          "adaptação",
          "mesmos",
          "parcial",
          "essa",
          "conter",
          "outro",
          "contenção",
          "gerando",
          "criando",
          "nossos",
          "corpos",
          "mais"
        ],
        "entities": [
          [
            "ação de resposta",
            "ORG"
          ],
          [
            "de nós mesmos",
            "PERSON"
          ],
          [
            "Essa",
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
            "excesso de problemas",
            "ORG"
          ],
          [
            "excesso de felic",
            "PERSON"
          ],
          [
            "qualquer ação de si mesmo",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "forma de \\ncontenção",
            "PERSON"
          ]
        ],
        "readability_score": 78.32835820895522,
        "semantic_density": 0,
        "word_count": 201,
        "unique_words": 131,
        "lexical_diversity": 0.6517412935323383
      },
      "preservation_score": 2.2273814224384078e-05
    },
    {
      "id": 1,
      "text": "energia, tendo facilidade em verificar o sintoma \\nem veias de maior circulação, se comemos \\nexcesso de comida, nossos corpos não \\nconseguem distribuir a quantidade de energia \\ningerida para o seu corpo.  \\nO nosso viver é saber valorizar o equilíbrio da \\nfísica quântica junto a física do físico. Qualquer \\nexcesso mental (quântico) causa um dano, assim \\ncomo qualquer excesso físico causa um dano \\nfísico. A nossa energia, mental e física, não \\nestando em equilíbrio afeta a minha própria \\npessoa, assim como a todos à  minha volta, \\nocasionando um viver melhor a própria vida, o \\nviver melhor com todos.",
      "position": 185298,
      "chapter": 7,
      "page": 150,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.649742268041237,
      "complexity_metrics": {
        "word_count": 97,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 24.25,
        "avg_word_length": 5.082474226804123,
        "unique_word_ratio": 0.7010309278350515,
        "avg_paragraph_length": 97.0,
        "punctuation_density": 0.13402061855670103,
        "line_break_count": 13,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "excesso",
          "viver",
          "física",
          "físico",
          "equilíbrio",
          "qualquer",
          "mental",
          "causa",
          "dano",
          "assim",
          "como",
          "minha",
          "própria",
          "todos",
          "melhor",
          "tendo",
          "facilidade",
          "verificar",
          "sintoma"
        ],
        "entities": [
          [
            "excesso de comida",
            "ORG"
          ],
          [
            "ingerida",
            "ORG"
          ],
          [
            "quântica",
            "NORP"
          ],
          [
            "Qualquer",
            "PERSON"
          ],
          [
            "qualquer excesso",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 86.35025773195876,
        "semantic_density": 0,
        "word_count": 97,
        "unique_words": 68,
        "lexical_diversity": 0.7010309278350515
      },
      "preservation_score": 4.700642612288848e-06
    }
  ],
  "book_name": "preconceito_Quântico_finalizado_editora[1].pdf",
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