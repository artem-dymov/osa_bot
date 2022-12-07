PGDMP     "    /            
    z            sova-dev-ubuntu     15.1 (Ubuntu 15.1-1.pgdg20.04+1)    15.0 7    '           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            (           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            )           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            *           1262    24604    sova-dev-ubuntu    DATABASE     y   CREATE DATABASE "sova-dev-ubuntu" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C.UTF-8';
 !   DROP DATABASE "sova-dev-ubuntu";
                postgres    false                        2615    32918    FBME    SCHEMA        CREATE SCHEMA "FBME";
    DROP SCHEMA "FBME";
                postgres    false            +           0    0    SCHEMA "FBME"    COMMENT     6   COMMENT ON SCHEMA "FBME" IS 'standard public schema';
                   postgres    false    7                        2615    32879    IPT    SCHEMA        CREATE SCHEMA "IPT";
    DROP SCHEMA "IPT";
                postgres    false            �            1259    32919    teachers    TABLE     �   CREATE TABLE "FBME".teachers (
    id integer NOT NULL,
    full_name text NOT NULL,
    type text DEFAULT 'NO DATA'::text NOT NULL,
    groups text[]
);
    DROP TABLE "FBME".teachers;
       FBME         heap    postgres    false    7            �            1259    32925    teachers_id_seq    SEQUENCE     �   CREATE SEQUENCE "FBME".teachers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE "FBME".teachers_id_seq;
       FBME          postgres    false    7    227            ,           0    0    teachers_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE "FBME".teachers_id_seq OWNED BY "FBME".teachers.id;
          FBME          postgres    false    228            �            1259    32926    votes_id_seq    SEQUENCE     �   CREATE SEQUENCE "FBME".votes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE "FBME".votes_id_seq;
       FBME          postgres    false    7            �            1259    32927    votes    TABLE     �   CREATE TABLE "FBME".votes (
    id integer DEFAULT nextval('"FBME".votes_id_seq'::regclass) NOT NULL,
    user_id integer,
    teacher_id integer,
    marks integer[],
    questions_id integer[]
);
    DROP TABLE "FBME".votes;
       FBME         heap    postgres    false    229    7            �            1259    32886    teachers    TABLE     �   CREATE TABLE "IPT".teachers (
    id integer NOT NULL,
    full_name text NOT NULL,
    type text DEFAULT 'NO DATA'::text NOT NULL,
    groups text[]
);
    DROP TABLE "IPT".teachers;
       IPT         heap    postgres    false    6            �            1259    32892    teachers_id_seq    SEQUENCE     �   CREATE SEQUENCE "IPT".teachers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE "IPT".teachers_id_seq;
       IPT          postgres    false    223    6            -           0    0    teachers_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE "IPT".teachers_id_seq OWNED BY "IPT".teachers.id;
          IPT          postgres    false    224            �            1259    32885    votes_id_seq    SEQUENCE     �   CREATE SEQUENCE "IPT".votes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE "IPT".votes_id_seq;
       IPT          postgres    false    6            �            1259    32880    votes    TABLE     �   CREATE TABLE "IPT".votes (
    id integer DEFAULT nextval('"IPT".votes_id_seq'::regclass) NOT NULL,
    user_id integer,
    teacher_id integer,
    marks integer[],
    questions_id integer[]
);
    DROP TABLE "IPT".votes;
       IPT         heap    postgres    false    222    6            �            1259    32804 	   questions    TABLE     b   CREATE TABLE public.questions (
    id integer NOT NULL,
    question_text text,
    type text
);
    DROP TABLE public.questions;
       public         heap    postgres    false            �            1259    32853    teachers    TABLE     [   CREATE TABLE public.teachers (
    id integer NOT NULL,
    full_name character varying
);
    DROP TABLE public.teachers;
       public         heap    postgres    false            �            1259    32842    teachers_id_seq    SEQUENCE     x   CREATE SEQUENCE public.teachers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.teachers_id_seq;
       public          postgres    false            �            1259    32809    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    tg_id bigint,
    username text,
    faculty text,
    "group" text
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    32814    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    217            .           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    218            �            1259    32911    votes    TABLE     �   CREATE TABLE public.votes (
    id integer NOT NULL,
    user_id integer,
    teacher_id integer,
    marks integer[],
    questions_id integer[]
);
    DROP TABLE public.votes;
       public         heap    postgres    false            �            1259    32910    votes_id_seq    SEQUENCE     u   CREATE SEQUENCE public.votes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.votes_id_seq;
       public          postgres    false            q           2604    32933    teachers id    DEFAULT     j   ALTER TABLE ONLY "FBME".teachers ALTER COLUMN id SET DEFAULT nextval('"FBME".teachers_id_seq'::regclass);
 :   ALTER TABLE "FBME".teachers ALTER COLUMN id DROP DEFAULT;
       FBME          postgres    false    228    227            o           2604    32894    teachers id    DEFAULT     h   ALTER TABLE ONLY "IPT".teachers ALTER COLUMN id SET DEFAULT nextval('"IPT".teachers_id_seq'::regclass);
 9   ALTER TABLE "IPT".teachers ALTER COLUMN id DROP DEFAULT;
       IPT          postgres    false    224    223            m           2604    32816    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217            !          0    32919    teachers 
   TABLE DATA           ?   COPY "FBME".teachers (id, full_name, type, groups) FROM stdin;
    FBME          postgres    false    227   ]8       $          0    32927    votes 
   TABLE DATA           M   COPY "FBME".votes (id, user_id, teacher_id, marks, questions_id) FROM stdin;
    FBME          postgres    false    230   9                 0    32886    teachers 
   TABLE DATA           >   COPY "IPT".teachers (id, full_name, type, groups) FROM stdin;
    IPT          postgres    false    223   �9                 0    32880    votes 
   TABLE DATA           L   COPY "IPT".votes (id, user_id, teacher_id, marks, questions_id) FROM stdin;
    IPT          postgres    false    221   6:                 0    32804 	   questions 
   TABLE DATA           <   COPY public.questions (id, question_text, type) FROM stdin;
    public          postgres    false    216   �:                 0    32853    teachers 
   TABLE DATA           1   COPY public.teachers (id, full_name) FROM stdin;
    public          postgres    false    220   F=                 0    32809    users 
   TABLE DATA           F   COPY public.users (id, tg_id, username, faculty, "group") FROM stdin;
    public          postgres    false    217   c=                  0    32911    votes 
   TABLE DATA           M   COPY public.votes (id, user_id, teacher_id, marks, questions_id) FROM stdin;
    public          postgres    false    226   >       /           0    0    teachers_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('"FBME".teachers_id_seq', 5, true);
          FBME          postgres    false    228            0           0    0    votes_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('"FBME".votes_id_seq', 7, true);
          FBME          postgres    false    229            1           0    0    teachers_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('"IPT".teachers_id_seq', 5, true);
          IPT          postgres    false    224            2           0    0    votes_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('"IPT".votes_id_seq', 7, true);
          IPT          postgres    false    222            3           0    0    teachers_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.teachers_id_seq', 1, true);
          public          postgres    false    219            4           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 20, true);
          public          postgres    false    218            5           0    0    votes_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.votes_id_seq', 1, false);
          public          postgres    false    225            �           2606    32935    votes poll_pkey 
   CONSTRAINT     M   ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_pkey PRIMARY KEY (id);
 9   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_pkey;
       FBME            postgres    false    230            �           2606    32937    teachers teachers_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY "FBME".teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY "FBME".teachers DROP CONSTRAINT teachers_pkey;
       FBME            postgres    false    227            {           2606    32896    votes poll_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY "IPT".votes
    ADD CONSTRAINT poll_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY "IPT".votes DROP CONSTRAINT poll_pkey;
       IPT            postgres    false    221            }           2606    32898    teachers teachers_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY "IPT".teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);
 ?   ALTER TABLE ONLY "IPT".teachers DROP CONSTRAINT teachers_pkey;
       IPT            postgres    false    223            u           2606    32820    questions questions_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.questions DROP CONSTRAINT questions_pkey;
       public            postgres    false    216            y           2606    32859    teachers teachers_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.teachers DROP CONSTRAINT teachers_pkey;
       public            postgres    false    220            w           2606    32822    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    217                       2606    32917    votes votes_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.votes
    ADD CONSTRAINT votes_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.votes DROP CONSTRAINT votes_pkey;
       public            postgres    false    226            �           2606    32938    votes poll_teacher_id_fkey    FK CONSTRAINT        ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES "FBME".teachers(id);
 D   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_teacher_id_fkey;
       FBME          postgres    false    227    3201    230            �           2606    32943    votes poll_user_id_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY "FBME".votes
    ADD CONSTRAINT poll_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 A   ALTER TABLE ONLY "FBME".votes DROP CONSTRAINT poll_user_id_fkey;
       FBME          postgres    false    217    230    3191            �           2606    32899    votes poll_teacher_id_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY "IPT".votes
    ADD CONSTRAINT poll_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES "IPT".teachers(id);
 C   ALTER TABLE ONLY "IPT".votes DROP CONSTRAINT poll_teacher_id_fkey;
       IPT          postgres    false    3197    221    223            �           2606    32904    votes poll_user_id_fkey    FK CONSTRAINT     u   ALTER TABLE ONLY "IPT".votes
    ADD CONSTRAINT poll_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 @   ALTER TABLE ONLY "IPT".votes DROP CONSTRAINT poll_user_id_fkey;
       IPT          postgres    false    3191    221    217            !   �   x�3�tJ�.�SpRp�,(JL.�LN�N*�54��2�0��.6_ثpa��1��f�\F�^�qa˅}.컰I�BHuNjrIi�b��Ɯ�\�va�Ş�.�+��j��I-�)�ea@�%�dpVC���L��@��B}|�Dm-W� �RI      $   i   x�M�A�0�𖍑�'�7o����Ң�ɲ3PH�P���
q�$(�*ԝ+� cA6g�&�tu���n�Ԥp��>��C kJ�������X��f��\-�         �   x�3�tJ�.�SpRp�,(JL.�LN�N*�54��2�0��.6_ثpa��1��f�\F�^�qa˅}.컰I�BHuNjrIi�b��Ɯ�\�va�Ş�.�+��j��I-�)�ea@�%�dpVC���L��@��B}|�Dm-W� �RI         i   x�M�A�0�𖍑�'�7o����Ң�ɲ3PH�P���
q�$(�*ԝ+� cA6g�&�tu���n�Ԥp��>��C kJ�������X��f��\-�         �  x��T�nA<{�b> L�����H !@���v�d	Y�	'���]��xv�����u61F9$��WUW�AG~I�$�J�:����;)u.�:�:u�e!���?�:v�6�\O`χ���2�5�`0d���\�Jg�c.��z��=�>%Obe�x8EV/����"`�(1>�aT�	�%4չ��;�,�C"K�1'~i�Oe�p�u>���􏒧1{
@�԰	���;b����B� >�u+��&-�d���XHiIC϶X��L��H�^���O�[[c<�z?x�<ߤ*	L��j+Utxj��ߍv�u����-Lu99�=a��ń��!?�{��n�%��.d�̨� �-�j��
Sh�S4�vl�y��z$B	�r�à輁��ѩyW�u��4���[%6Hw���ߑ�R�_�&���z��+grH��3G�ta明���#�A���������b�U��`�һv����&����%����O����qG����,� �;%���1{e��0gA4Aqʁ��ъ+�f�I��w���������A�J
��3�l�Ê�#3N�a�ePm�W�����f����m(	�!=���
�v�ͺ
#���U�\nr�zm���^�$�c�z            x������ � �         �   x�}б
�@�9y咻k�[,T�.�J���U��[+�7� ��%�� ic mھ�o���l�]As������Uǡ�>!�w���ǆ���qn�ߨ�Xȝ�'BNJ��%� ��+ׇM�(���z�<�|�q�?�avaN���h(�Oa9G���l0             x������ � �     