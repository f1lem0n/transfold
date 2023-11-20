# import shutil
# from pathlib import Path

# from modules.downloaders import download_all_protein_sequences
# from modules.scopes_parser import get_scope_df

# # do not change these params
# OUTPUT_PATH = Path("tests/data").absolute()


# def test_download_all_protein_sequences():
#     # when file does not exist and skipping
#     # one entry because it does not exist
#     assert (
#         download_all_protein_sequences(
#             OUTPUT_PATH, get_scope_df(OUTPUT_PATH / "test_scopes.tsv")
#         )
#         == 1
#     )
#     # check if all the files are created from existing pdb ids
#     assert (OUTPUT_PATH / "protein_seq").exists()
#     for pdb_id in [
#         "1ux8",
#         "1dlw",
#         "1uvy",
#         "1dly",
#         "1uvx",
#         "2gkm",
#         "2gkm",
#         "2gl3",
#         "2gl3",
#         "1idr",
#     ]:
#         assert (OUTPUT_PATH / "protein_seq" / f"{pdb_id}.fasta").exists()
#     # when all files already exist
#     assert (
#         download_all_protein_sequences(
#             OUTPUT_PATH, get_scope_df(OUTPUT_PATH / "test_scopes.tsv")
#         )
#         == 1
#     )
#     # this one should not exist because it has incorrect pdb id
#     assert not (OUTPUT_PATH / "protein_seq" / "0000.fasta").exists()
#     # clean up
#     shutil.rmtree(OUTPUT_PATH / "protein_seq")
